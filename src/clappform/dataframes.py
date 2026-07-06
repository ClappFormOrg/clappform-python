"""Collection and saved-query handles — the DataFrame-flavoured surface.

This is the ergonomic layer people actually reach for:

    col = cf.data.collection("sales_orders")   # slug or UUID (resolved via :mod:`clappform._resolve`)
    df = col.read(where={"status": "open"}, fields=["id", "amount"], limit=1000)
    col.append(df); col.update(df); col.upsert(df, on="order_id")

A handle holds only ``(client, reference)`` — no connection, no state — and
every flow runs over the streaming data RPCs through the client's transport.
Reads go through :class:`ReadResult`, the seam future output surfaces
(``to_polars``/``to_arrow``) plug into: ``read()`` is literally
``fetch().to_pandas()``.

Encoding lives in :mod:`clappform._codec` as records in / records out, so this
module never touches JSON directly and pandas is applied only at the very edge
(:meth:`ReadResult.to_pandas`). ``read()`` keeps ``_id`` as an ordinary column,
so a read -> mutate -> ``update()`` round-trip keys on it with no special
handling from the caller.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator, Mapping, Sequence
from typing import TYPE_CHECKING, Any

from clappform import _codec
from clappform._codec import Record
from clappform._errors import ClappformError, NotFoundError

if TYPE_CHECKING:
    import pandas as pd

    from clappform._client import Clappform

ProgressCallback = Callable[[int], None]


def _require_pandas() -> Any:
    """Import pandas, turning the ImportError into an actionable message."""
    try:
        import pandas as pd
    except ImportError as exc:  # pragma: no cover - exercised via monkeypatch
        raise ClappformError(
            "pandas is required for DataFrame conversion; "
            "install it with: pip install clappform[pandas]"
        ) from exc
    return pd


def _records_from_frame(df: pd.DataFrame) -> list[Record]:
    """Turn a DataFrame into plain records (the codec's input form).

    ``to_dict("records")`` yields one dict per row with native Python scalars;
    the codec then normalises ``NaN``/``NaT``/datetimes on encode, so nothing
    pandas-specific leaks past this boundary.
    """
    return df.to_dict("records")


class ReadResult:
    """A lazily-materialised result set from ``AggregateStream``.

    Wraps the stream of ``(format, bytes)`` chunks the server sends and exposes
    it as records (:meth:`__iter__`, :meth:`iter_batches`) or a pandas frame
    (:meth:`to_pandas`). It is single-pass: the underlying gRPC stream is
    consumed once, so iterate or convert exactly one way. Materialising the
    same result twice raises rather than silently returning an empty set.

    Shipping this now (rather than returning a DataFrame straight from
    ``read()``) is deliberate: ``to_polars`` / ``to_arrow`` / the Arrow
    PyCapsule protocol land as new methods here without changing any existing
    return type, and the batch-wise internals let a future Arrow reader map one
    Arrow batch per gRPC chunk.
    """

    __slots__ = ("_chunks", "_consumed")

    def __init__(self, chunks: Iterable[tuple[_codec.ChunkFormat, bytes]]) -> None:
        self._chunks = iter(chunks)
        self._consumed = False

    def _claim(self) -> None:
        if self._consumed:
            raise ClappformError(
                "this ReadResult has already been consumed; a result set streams "
                "once — call read()/fetch() again for a fresh one"
            )
        self._consumed = True

    def __iter__(self) -> Iterator[Record]:
        """Yield every record across all chunks, one row at a time."""
        self._claim()
        return _codec.records_from_chunks(self._chunks)

    def iter_batches(self) -> Iterator[list[Record]]:
        """Yield one list of records per gRPC chunk (memory-bounded reads)."""
        self._claim()
        for fmt, data in self._chunks:
            yield _codec.bytes_to_records(data, fmt)

    def to_pandas(self) -> pd.DataFrame:
        """Materialise the whole result set as a pandas DataFrame.

        ``_id`` stays an ordinary column so the frame round-trips through
        :meth:`CollectionHandle.update`. An empty result yields an empty frame.
        """
        pd = _require_pandas()
        records = list(self)
        return pd.DataFrame.from_records(records)


class _AggregateReader:
    """Shared read machinery for collection and saved-query handles.

    Both handles read through ``AggregateStream``; they differ only in which
    request fields they fill (a collection sends ``collection`` + ``pipeline``,
    a saved query sends ``query``). This centralises the streaming, the
    ``(format, bytes)`` adaptation, and the stale-UUID re-resolution retry.
    """

    # Provided by the concrete handles (declared in their __slots__).
    _client: Clappform
    _location: str

    def _stream(
        self,
        *,
        collection: str | None,
        pipeline: bytes | None,
        query: str | None,
        batch_size: int | None,
        timeout: float | None,
    ) -> Iterator[tuple[_codec.ChunkFormat, bytes]]:
        responses = self._client.data.aggregate.aggregate_stream(
            collection=collection,
            pipeline=pipeline,
            query=query,
            batch_size=batch_size,
            location=self._location,
            timeout=timeout,
        )
        for response in responses:
            # The stream carries only JSON today; the codec branches on the
            # format so an Arrow chunk type slots in without changing callers.
            yield _codec.ChunkFormat.JSON, response.data

    def _read_reresolving(
        self,
        open_stream: Callable[[], Iterator[tuple[_codec.ChunkFormat, bytes]]],
        on_stale: Callable[[], None],
    ) -> Iterator[tuple[_codec.ChunkFormat, bytes]]:
        """Open a read stream, re-resolving once if the id is stale.

        ``AggregateStream`` is lazy: the request is not sent until the returned
        iterator is first advanced, and the transport surfaces a server
        ``NOT_FOUND`` as :class:`NotFoundError` at that point. So the first
        chunk is pulled here to probe. If it fails ``NOT_FOUND``, ``on_stale``
        drops the cached id, and a second stream is opened against the freshly
        resolved id — this is the one re-resolution the slug contract promises.

        The retry deliberately covers only a ``NOT_FOUND`` raised *before* any
        row reaches the caller (the probe). Once the first chunk has been
        handed out, retrying would replay already-delivered rows, so a
        ``NOT_FOUND`` on a later chunk propagates unchanged rather than
        silently duplicating data. A directly-supplied UUID has no cache entry,
        so ``on_stale`` is a no-op and the second open simply fails the same way.
        """
        stream = open_stream()
        try:
            first = next(stream)
        except StopIteration:
            return
        except NotFoundError:
            on_stale()
            yield from open_stream()
            return
        yield first
        yield from stream


def _compile_pipeline(
    where: Mapping[str, Any] | None,
    fields: Sequence[str] | None,
    limit: int | None,
) -> list[dict[str, Any]]:
    """Compile ``where``/``fields``/``limit`` sugar into a Mongo pipeline.

    These kwargs are purely client-side — the API never sees them. Each maps
    to one stage in a plain aggregation pipeline (``$match`` / ``$project`` /
    ``$limit``), producing exactly what an equivalent ``aggregate()`` call
    would send. Order matches Mongo semantics: filter, then project, then cap.
    """
    pipeline: list[dict[str, Any]] = []
    if where:
        pipeline.append({"$match": dict(where)})
    if fields:
        pipeline.append({"$project": {field: 1 for field in fields}})
    if limit is not None:
        if limit < 0:
            raise ValueError(f"limit must be non-negative, got {limit}")
        pipeline.append({"$limit": limit})
    return pipeline


class CollectionHandle(_AggregateReader):
    """A handle to one collection: reads, writes, and ad-hoc aggregation.

    Obtained from ``cf.data.collection(ref)`` where ``ref`` is a slug or a
    UUID (resolved on first use, cached per location). Holds nothing but the
    client and the resolved collection id.
    """

    __slots__ = ("_client", "_ref", "_location", "_id")

    def __init__(self, client: Clappform, ref: str) -> None:
        self._client = client
        self._ref = ref
        self._location = client.location
        self._id: str | None = None

    @property
    def collection_id(self) -> str:
        """The resolved collection UUID (resolves + caches on first access)."""
        if self._id is None:
            self._id = self._client._resolver.collection_id(self._ref, self._location)
        return self._id

    def __repr__(self) -> str:
        resolved = f" -> {self._id}" if self._id is not None else ""
        return f"CollectionHandle({self._ref!r}{resolved}, location={self._location!r})"

    # -- reads -----------------------------------------------------------

    def fetch(
        self,
        *,
        where: Mapping[str, Any] | None = None,
        fields: Sequence[str] | None = None,
        limit: int | None = None,
        pipeline: Sequence[Mapping[str, Any]] | None = None,
        batch_size: int | None = None,
        timeout: float | None = None,
    ) -> ReadResult:
        """Stream the collection into a :class:`ReadResult`.

        ``where``/``fields``/``limit`` are client-side sugar compiled into a
        ``$match``/``$project``/``$limit`` pipeline. ``pipeline=`` supplies a
        full aggregation pipeline instead and is mutually exclusive with the
        sugar — passing both is a caller error.
        """
        if pipeline is not None and (where or fields or limit is not None):
            raise ValueError("pass either pipeline= or the where/fields/limit sugar, not both")
        stages = (
            [dict(stage) for stage in pipeline]
            if pipeline is not None
            else _compile_pipeline(where, fields, limit)
        )
        encoded = _codec.encode_pipeline(stages)
        chunks = self._read_with_retry(encoded, batch_size, timeout)
        return ReadResult(chunks)

    def read(
        self,
        *,
        where: Mapping[str, Any] | None = None,
        fields: Sequence[str] | None = None,
        limit: int | None = None,
        batch_size: int | None = None,
        timeout: float | None = None,
    ) -> pd.DataFrame:
        """The whole collection (or a filtered slice) as a pandas DataFrame.

        Exactly ``fetch(...).to_pandas()``. ``_id`` is kept as a column so the
        frame can be mutated and passed straight to :meth:`update`.
        """
        return self.fetch(
            where=where,
            fields=fields,
            limit=limit,
            batch_size=batch_size,
            timeout=timeout,
        ).to_pandas()

    def iter_batches(
        self,
        *,
        where: Mapping[str, Any] | None = None,
        fields: Sequence[str] | None = None,
        limit: int | None = None,
        batch_size: int | None = None,
        timeout: float | None = None,
    ) -> Iterator[list[Record]]:
        """Stream records in memory-bounded batches (one list per gRPC chunk).

        ``batch_size`` asks the server to cap each chunk's row count; the
        client yields whatever chunking the server sends back.
        """
        return self.fetch(
            where=where,
            fields=fields,
            limit=limit,
            batch_size=batch_size,
            timeout=timeout,
        ).iter_batches()

    def aggregate(
        self,
        pipeline: Sequence[Mapping[str, Any]],
        *,
        batch_size: int | None = None,
        timeout: float | None = None,
    ) -> pd.DataFrame:
        """Run a caller-supplied aggregation pipeline, returning a DataFrame.

        The pipeline is passed through untouched — use this for Elastic-backed
        collections (whose DSL the ``where``/``fields`` sugar does not emit) or
        any stage the sugar does not cover (``$group``, ``$sort``, ...).
        """
        return self.fetch(pipeline=pipeline, batch_size=batch_size, timeout=timeout).to_pandas()

    def _read_with_retry(
        self, pipeline: bytes, batch_size: int | None, timeout: float | None
    ) -> Iterator[tuple[_codec.ChunkFormat, bytes]]:
        """Stream chunks, re-resolving the collection once on a stale UUID.

        A cached slug->UUID mapping can go stale (the collection was recreated
        or its slug remapped); the first read then fails ``NOT_FOUND``. When
        the id came from a slug, drop the cache entry and resolve again before
        surfacing the error. A UUID passed directly is not retried — there is
        nothing to re-resolve.
        """

        def _open() -> Iterator[tuple[_codec.ChunkFormat, bytes]]:
            return self._stream(
                collection=self.collection_id,
                pipeline=pipeline,
                query=None,
                batch_size=batch_size,
                timeout=timeout,
            )

        def _on_stale() -> None:
            self._client._resolver.invalidate_collection(self._ref, self._location)
            self._id = None

        return self._read_reresolving(_open, _on_stale)

    # -- writes ----------------------------------------------------------

    def append(
        self,
        df: pd.DataFrame,
        *,
        chunk_rows: int = _codec.DEFAULT_CHUNK_ROWS,
        progress: ProgressCallback | None = None,
        timeout: float | None = None,
    ) -> int:
        """Insert every row of ``df`` as new documents. Returns rows written.

        Uploads stream in chunks of ``chunk_rows`` (a failed chunk is
        retryable at the flow level, not a whole-frame resend). ``progress`` is
        invoked with the cumulative row count after each chunk — handy for a
        notebook progress bar.
        """
        insert_pb2 = _import("clappform.gen.clappform.data.v1.insert.insert_pb2")
        records = _records_from_frame(df)

        def _requests() -> Iterator[Any]:
            written = 0
            for chunk in _codec.chunk_records(records, chunk_rows):
                yield insert_pb2.InsertRequest(collection=self.collection_id, data=chunk)
                written += _rows_in(chunk)
                if progress is not None:
                    progress(written)

        total = 0
        for response in self._client.data.insert.insert_many(
            _requests(), location=self._location, timeout=timeout
        ):
            total += response.processed_count
        return total

    def update(
        self,
        df: pd.DataFrame,
        *,
        on: str = "_id",
        chunk_rows: int = _codec.DEFAULT_CHUNK_ROWS,
        timeout: float | None = None,
    ) -> int:
        """Update existing documents, matched by the ``on`` column (default ``_id``).

        Every row must carry the ``on`` key. Because ``read()`` keeps ``_id`` as
        a column, the common case — read, mutate other columns, ``update(df)`` —
        needs no argument at all.
        """
        update_pb2 = _import("clappform.gen.clappform.data.v1.update.update_pb2")
        records = _records_from_frame(df)
        _require_key(records, on, "update")

        def _requests() -> Iterator[Any]:
            for chunk in _codec.chunk_records(records, chunk_rows):
                yield update_pb2.UpdateRequestByOid(collection=self.collection_id, data=chunk)

        self._client.data.update.update_many(_requests(), location=self._location, timeout=timeout)
        return len(records)

    def upsert(
        self,
        df: pd.DataFrame,
        *,
        on: str,
        chunk_rows: int = _codec.DEFAULT_CHUNK_ROWS,
        timeout: float | None = None,
    ) -> int:
        """Insert-or-update every row keyed on the business column ``on``.

        Uses ``SyncManyByField``: rows whose ``on`` value already exists are
        updated, the rest inserted. ``on`` is required — an upsert has no
        default key the way :meth:`update` does.
        """
        sync_pb2 = _import("clappform.gen.clappform.data.v1.sync.sync_pb2")
        records = _records_from_frame(df)
        _require_key(records, on, "upsert")

        def _requests() -> Iterator[Any]:
            for chunk in _codec.chunk_records(records, chunk_rows):
                yield sync_pb2.SyncRequestByField(
                    collection=self.collection_id, data=chunk, field_name=on
                )

        self._client.data.sync.sync_many_by_field(
            _requests(), location=self._location, timeout=timeout
        )
        return len(records)

    def replace_where(
        self,
        where: Mapping[str, Any],
        set_values: Mapping[str, Any],
        *,
        timeout: float | None = None,
    ) -> None:
        """Set ``set_values`` on every document matching the ``where`` filter.

        A single server-side ``$set`` over the matched documents
        (``UpdateManyByQuery``) — no data is round-tripped through the client.
        """
        self._client.data.update.update_many_by_query(
            collection=self.collection_id,
            query=_codec.encode_pipeline(dict(where)),
            set_values=_codec.encode_pipeline(dict(set_values)),
            location=self._location,
            timeout=timeout,
        )

    def delete(
        self,
        *,
        where: Mapping[str, Any] | None = None,
        oids: Sequence[str] | None = None,
        timeout: float | None = None,
    ) -> None:
        """Delete documents by ``where`` filter or by explicit ``oids``.

        Exactly one of ``where`` / ``oids`` must be given. To wipe the whole
        collection use :meth:`clear`, which is explicit by design so a full
        delete is never an accident of an empty filter.
        """
        if (where is None) == (oids is None):
            raise ValueError("pass exactly one of where= or oids=")
        if where is not None and not where:
            # An empty filter matches every document. Deleting the whole
            # collection must be explicit, so refuse it here and point at the
            # deliberate full-wipe method rather than let an empty where=
            # silently clear everything.
            raise ValueError(
                "where={} matches every document; use clear() to wipe the "
                "whole collection explicitly"
            )
        if oids is not None:
            self._client.data.delete.delete_many_by_oids(
                collection=self.collection_id,
                oids=list(oids),
                location=self._location,
                timeout=timeout,
            )
            return
        assert where is not None  # guaranteed by the XOR check above
        self._client.data.delete.delete_many_by_query(
            collection=self.collection_id,
            query=_codec.encode_pipeline(dict(where)),
            location=self._location,
            timeout=timeout,
        )

    def clear(self, *, timeout: float | None = None) -> None:
        """Remove every document from the collection (an explicit full wipe)."""
        self._client.data.delete.clear(
            collection=self.collection_id, location=self._location, timeout=timeout
        )


class QueryHandle(_AggregateReader):
    """A handle to a saved server-side query: read-only aggregation.

    Obtained from ``cf.data.query(ref)`` where ``ref`` is the query's name or
    UUID. A saved query already carries its own collection and pipeline, so the
    handle sends only the ``query`` field on ``AggregateStream`` — no
    collection, no pipeline, and no write surface.
    """

    __slots__ = ("_client", "_ref", "_location", "_id")

    def __init__(self, client: Clappform, ref: str) -> None:
        self._client = client
        self._ref = ref
        self._location = client.location
        self._id: str | None = None

    @property
    def query_id(self) -> str:
        """The resolved saved-query UUID (resolves + caches on first access)."""
        if self._id is None:
            self._id = self._client._resolver.query_id(self._ref, self._location)
        return self._id

    def __repr__(self) -> str:
        resolved = f" -> {self._id}" if self._id is not None else ""
        return f"QueryHandle({self._ref!r}{resolved}, location={self._location!r})"

    def fetch(self, *, batch_size: int | None = None, timeout: float | None = None) -> ReadResult:
        """Run the saved query and stream its result into a :class:`ReadResult`."""
        return ReadResult(self._read_with_retry(batch_size, timeout))

    def read(self, *, batch_size: int | None = None, timeout: float | None = None) -> pd.DataFrame:
        """Run the saved query and return its result as a pandas DataFrame."""
        return self.fetch(batch_size=batch_size, timeout=timeout).to_pandas()

    def iter_batches(
        self, *, batch_size: int | None = None, timeout: float | None = None
    ) -> Iterator[list[Record]]:
        """Stream the saved query's result in memory-bounded batches."""
        return self.fetch(batch_size=batch_size, timeout=timeout).iter_batches()

    def _read_with_retry(
        self, batch_size: int | None, timeout: float | None
    ) -> Iterator[tuple[_codec.ChunkFormat, bytes]]:
        """Stream chunks, re-resolving the query once on a stale UUID."""

        def _open() -> Iterator[tuple[_codec.ChunkFormat, bytes]]:
            return self._stream(
                collection=None,
                pipeline=None,
                query=self.query_id,
                batch_size=batch_size,
                timeout=timeout,
            )

        def _on_stale() -> None:
            self._client._resolver.invalidate_query(self._ref, self._location)
            self._id = None

        return self._read_reresolving(_open, _on_stale)


# -- small helpers -------------------------------------------------------


def _import(module: str) -> Any:
    """Import a generated pb2 module by dotted path (kept lazy and local)."""
    import importlib

    return importlib.import_module(module)


def _rows_in(chunk: bytes) -> int:
    """Count the records a JSON chunk carries (for progress reporting)."""
    return len(_codec.bytes_to_records(chunk))


def _require_key(records: list[Record], key: str, op: str) -> None:
    """Fail fast if any record lacks the join key an update/upsert needs."""
    for record in records:
        if key not in record:
            raise ValueError(f"{op} keyed on {key!r} but a row is missing that column")
