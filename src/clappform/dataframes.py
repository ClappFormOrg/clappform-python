"""Collection and saved-query handles: the DataFrame-flavoured surface.

This is the ergonomic layer people actually reach for:

    col = cf.data.collection("sales_orders")   # slug or UUID (resolved in _resolve)
    df = col.read()                             # whole collection
    df = col.read(pipeline=[{"$match": {"status": "open"}}])   # filtered slice
    col.append(df); col.update(df); col.upsert(df, on="order_id")

A handle holds only ``(client, reference)``: no connection, no state, and
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

import warnings
from collections.abc import Callable, Generator, Iterable, Iterator, Mapping, Sequence
from typing import TYPE_CHECKING, Any

from clappform import _codec
from clappform._codec import Record
from clappform._errors import ClappformError, NotFoundError
from clappform.gen.clappform.data.v1.insert import insert_pb2
from clappform.gen.clappform.data.v1.sync import sync_pb2
from clappform.gen.clappform.data.v1.update import update_pb2

if TYPE_CHECKING:
    import pandas as pd

    from clappform._client import Clappform

ProgressCallback = Callable[[int], None]

# A chunk stream the read machinery can close (cancelling the call) when the
# caller stops early.
_Chunks = Generator[tuple[_codec.ChunkFormat, bytes], None, None]


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


def _require_pyarrow() -> Any:
    """Import pyarrow, turning the ImportError into an actionable message."""
    try:
        import pyarrow as pa
    except ImportError as exc:  # pragma: no cover - exercised via monkeypatch
        raise ClappformError(
            "pyarrow is required for Arrow conversion; "
            "install it with: pip install clappform[arrow]"
        ) from exc
    return pa


def _require_polars() -> Any:
    """Import polars, turning the ImportError into an actionable message."""
    try:
        import polars as pl
    except ImportError as exc:  # pragma: no cover - exercised via monkeypatch
        raise ClappformError(
            "polars is required for Polars conversion; "
            "install it with: pip install clappform[polars]"
        ) from exc
    return pl


# The server does not yet emit Arrow IPC on the streaming data plane, so the
# columnar surfaces below cannot produce a result even with pyarrow/polars
# installed. They exist now, failing loudly rather than as AttributeError, so
# the names are reserved and callers discover the capability; they light up
# (as a purely additive change) once a cluster negotiates the Arrow format.
_ARROW_NOT_READY = (
    "Arrow output is not available yet: this client version always reads JSON, "
    "and Arrow lands as an additive surface once server Arrow support ships on "
    "your cluster. Track the v6 Arrow read-path work for availability."
)


def _records_from_frame(df: pd.DataFrame, op: str) -> list[Record]:
    """Turn a DataFrame into plain records (the codec's input form).

    ``to_dict("records")`` yields one dict per row with native Python scalars;
    the codec then normalises ``NaN``/``NaT``/datetimes on encode, so nothing
    pandas-specific leaks past this boundary.

    Records carry columns only, so the index is not written. An unnamed index
    is positional (a filter's leftover row labels) and is dropped. A named one
    (``set_index("order_id")``, a ``groupby`` result) holds data, so it is
    refused rather than lost.
    """
    named = [name for name in df.index.names if name is not None]
    if named:
        raise ValueError(
            f"{op}() writes columns only and would drop the index {named}; call "
            f"df.reset_index() to write it as columns, or df.reset_index(drop=True) "
            f"to discard it"
        )
    return df.to_dict("records")


class ReadResult:
    """A lazily-materialised result set from ``AggregateStream``.

    Wraps the stream of ``(format, bytes)`` chunks the server sends and exposes
    it as records (:meth:`__iter__`, :meth:`iter_batches`) or a pandas frame
    (:meth:`to_pandas`). It is single-pass: the underlying gRPC stream is
    consumed once, so iterate or convert exactly one way. Materialising the
    same result twice raises rather than silently returning an empty set.

    ``to_arrow`` / ``to_polars`` are reserved and raise ``NotImplementedError``
    until server Arrow support ships. The Arrow PyCapsule protocol
    (``__arrow_c_stream__``) is deliberately *not* defined: Polars, DuckDB and
    pyarrow probe for it and would call a stub that can only raise.
    """

    __slots__ = ("_chunks", "_consumed")

    def __init__(self, chunks: Iterable[tuple[_codec.ChunkFormat, bytes]]) -> None:
        self._chunks = iter(chunks)
        self._consumed = False

    def _claim(self) -> None:
        if self._consumed:
            raise ClappformError(
                "this ReadResult has already been consumed; a result set streams "
                "once; call read()/fetch() again for a fresh one"
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

    def to_arrow(self) -> Any:
        """Materialise the result set as a ``pyarrow.Table`` (reserved).

        The fast, zero-per-row-object base the other columnar surfaces build on:
        once the server negotiates Arrow IPC, one gRPC chunk maps to one Arrow
        record batch and this returns a ``Table`` without ever materialising
        Python rows. Requires ``pip install clappform[arrow]``.

        Reserved for the v6 Arrow read path; raises until server Arrow support
        ships (the JSON path via :meth:`to_pandas` handles today's reads).
        """
        _require_pyarrow()
        raise NotImplementedError(_ARROW_NOT_READY)

    def to_polars(self) -> Any:
        """Materialise the result set as a ``polars.DataFrame`` (reserved).

        Built on :meth:`to_arrow` (zero-copy ``pl.from_arrow``), so once
        implemented it needs pyarrow as well as polars, so install
        ``clappform[polars,arrow]`` (or ``clappform[all]``). This stub only
        checks for polars, as it raises before any Arrow conversion runs.

        Reserved for the v6 Arrow read path; raises until server Arrow support
        ships.
        """
        _require_polars()
        raise NotImplementedError(_ARROW_NOT_READY)


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
    ) -> _Chunks:
        responses = self._client.data.aggregate.aggregate_stream(
            collection=collection,
            pipeline=pipeline,
            query=query,
            batch_size=batch_size,
            location=self._location,
            timeout=timeout,
        )
        try:
            for response in responses:
                # The stream carries only JSON today; the codec branches on the
                # format so an Arrow chunk type slots in without changing callers.
                yield _codec.ChunkFormat.JSON, response.data
        finally:
            # Closing the transport's iterator cancels the call when the
            # caller stopped reading before the end.
            close = getattr(responses, "close", None)
            if close is not None:
                close()

    def _read_reresolving(
        self,
        open_stream: Callable[[], _Chunks],
        on_stale: Callable[[], None],
    ) -> Iterator[tuple[_codec.ChunkFormat, bytes]]:
        """Open a read stream, re-resolving once if the id is stale.

        ``AggregateStream`` is lazy: the request is not sent until the returned
        iterator is first advanced, and the transport surfaces a server
        ``NOT_FOUND`` as :class:`NotFoundError` at that point. So the first
        chunk is pulled here to probe. If it fails ``NOT_FOUND``, ``on_stale``
        drops the cached id, and a second stream is opened against the freshly
        resolved id. This is the one re-resolution the slug contract promises.

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
        try:
            yield first
            yield from stream
        finally:
            stream.close()


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
        pipeline: Sequence[Mapping[str, Any]] | None = None,
        batch_size: int | None = None,
        timeout: float | None = None,
    ) -> ReadResult:
        """Stream the collection into a :class:`ReadResult`.

        ``pipeline=`` is an aggregation pipeline applied server-side; omit it to
        stream the whole collection. The pipeline is sent untouched, so it must
        be in the syntax the collection's backend expects (Mongo stages for a
        Mongo-backed collection, Elastic DSL for an Elastic-backed one).
        :meth:`read` / :meth:`aggregate` are the DataFrame-returning twins.
        """
        stages = [dict(stage) for stage in pipeline] if pipeline is not None else []
        encoded = _codec.encode_pipeline(stages)
        chunks = self._read_with_retry(encoded, batch_size, timeout)
        return ReadResult(chunks)

    def read(
        self,
        *,
        pipeline: Sequence[Mapping[str, Any]] | None = None,
        batch_size: int | None = None,
        timeout: float | None = None,
    ) -> pd.DataFrame:
        """The whole collection (or a ``pipeline``-filtered slice) as a DataFrame.

        Exactly ``fetch(...).to_pandas()``. Omit ``pipeline`` for the whole
        collection, or pass one to filter/project/reshape server-side. ``_id``
        is kept as a column so the frame can be mutated and passed straight to
        :meth:`update`.
        """
        return self.fetch(
            pipeline=pipeline,
            batch_size=batch_size,
            timeout=timeout,
        ).to_pandas()

    def iter_batches(
        self,
        *,
        pipeline: Sequence[Mapping[str, Any]] | None = None,
        batch_size: int | None = None,
        timeout: float | None = None,
    ) -> Iterator[list[Record]]:
        """Stream records in memory-bounded batches (one list per gRPC chunk).

        ``batch_size`` asks the server to cap each chunk's row count; the
        client yields whatever chunking the server sends back. ``pipeline=``
        filters/reshapes server-side, exactly as on :meth:`read`.
        """
        return self.fetch(
            pipeline=pipeline,
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

        The DataFrame-returning form of ``fetch(pipeline=...)``. The pipeline is
        passed through untouched, so use the syntax the collection's backend
        expects: Mongo stages (``$match``, ``$project``, ``$group``, ``$sort``,
        ...) for a Mongo-backed collection, Elastic DSL for an Elastic-backed one.
        """
        return self.fetch(pipeline=pipeline, batch_size=batch_size, timeout=timeout).to_pandas()

    def _read_with_retry(
        self, pipeline: bytes, batch_size: int | None, timeout: float | None
    ) -> Iterator[tuple[_codec.ChunkFormat, bytes]]:
        """Stream chunks, re-resolving the collection once on a stale UUID.

        A cached slug->UUID mapping can go stale (the collection was recreated
        or its slug remapped); the first read then fails ``NOT_FOUND``. When
        the id came from a slug, drop the cache entry and resolve again before
        surfacing the error. A UUID passed directly is not retried, because there is
        nothing to re-resolve.
        """

        def _open() -> _Chunks:
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

        Rows stream to the server in chunks of ``chunk_rows`` over one
        ``InsertMany`` call, and the server acknowledges each chunk.
        ``progress`` is called with the cumulative count of *acknowledged*
        rows after each chunk, handy for a notebook progress bar.

        ``append`` is not idempotent. If it fails partway, the chunks already
        acknowledged stay inserted, and running it again inserts them again.
        The raised error's ``rows_written`` says how many rows the server
        acknowledged, i.e. ``df.iloc[err.rows_written:]`` is what is left.
        For a load you may need to re-run, use :meth:`upsert` on a business
        key instead.

        The frame must not carry an ``_id`` column: the server assigns ids and
        rejects inserts that bring their own. To write rows read from a
        collection back by ``_id``, use :meth:`update`.
        """
        if "_id" in df.columns:
            raise ValueError(
                "append() inserts new documents and the server rejects rows that "
                "carry an _id; drop it first with df.drop(columns='_id'), or use "
                "update() to write rows back by _id"
            )
        records = _records_from_frame(df, "append")
        collection = self.collection_id

        def _requests() -> Iterator[Any]:
            for payload, _rows in _codec.chunk_records(records, chunk_rows):
                yield insert_pb2.InsertRequest(collection=collection, data=payload)

        total = 0
        try:
            for response in self._client.data.insert.insert_many(
                _requests(), location=self._location, timeout=timeout
            ):
                total += response.processed_count
                if progress is not None:
                    progress(total)
        except ClappformError as exc:
            exc.rows_written = total
            raise
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

        Each row's other columns are set on the matched document; fields the
        frame does not carry are left alone. ``on="_id"`` matches on the
        document id (``UpdateMany``); any other column matches on that field's
        value (``UpdateManyByField``). Every row must have a value for ``on``.
        Because ``read()`` keeps ``_id`` as a column, the common case (read,
        mutate other columns, ``update(df)``) needs no argument at all.

        Returns the number of rows sent; the server reports no match count.
        Raises :class:`~clappform.NotSupportedError` on a cluster that does
        not serve these RPCs yet.
        """
        records = _records_from_frame(df, "update")
        _require_key(records, on, "update")
        collection = self.collection_id
        chunks = _codec.chunk_records(records, chunk_rows)

        if on == "_id":
            by_oid = (
                update_pb2.UpdateRequestByOid(collection=collection, data=payload)
                for payload, _rows in chunks
            )
            self._client.data.update.update_many(
                by_oid, location=self._location, timeout=timeout
            )
        else:
            by_field = (
                update_pb2.UpdateRequestByField(
                    collection=collection, data=payload, field_name=on
                )
                for payload, _rows in chunks
            )
            self._client.data.update.update_many_by_field(
                by_field, location=self._location, timeout=timeout
            )
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

        Uses ``SyncManyByField``: a document whose ``on`` value matches a row is
        *replaced* by that row (fields the frame does not carry are dropped;
        the document keeps its ``_id``), and unmatched rows are inserted. So
        re-running the same upsert converges instead of duplicating. Send
        every field the documents should keep. ``on`` is required, because an upsert has no
        default key the way :meth:`update` does, and every row needs a value
        for it. Returns the number of rows sent.

        The frame must not carry an ``_id`` column. The server writes a row's
        ``_id`` into the replacement document, and ``read()`` returns ``_id``
        as a string, which does not equal the stored ObjectId: a matched row
        fails as an altered ``_id`` and an unmatched row is inserted under a
        string id. Drop it with ``df.drop(columns="_id")``.
        """
        if "_id" in df.columns:
            raise ValueError(
                "upsert() cannot write an _id column: read() returns _id as a string, "
                "which the server cannot write over the stored ObjectId; drop it with "
                "df.drop(columns='_id') and key on a business column"
            )
        records = _records_from_frame(df, "upsert")
        _require_key(records, on, "upsert")
        collection = self.collection_id

        requests = (
            sync_pb2.SyncRequestByField(collection=collection, data=payload, field_name=on)
            for payload, _rows in _codec.chunk_records(records, chunk_rows)
        )
        self._client.data.sync.sync_many_by_field(
            requests, location=self._location, timeout=timeout
        )
        return len(records)

    def update_where(
        self,
        where: Mapping[str, Any],
        set_values: Mapping[str, Any],
        *,
        timeout: float | None = None,
    ) -> None:
        """Set ``set_values`` on every document matching the ``where`` filter.

        A single server-side ``$set`` over the matched documents
        (``UpdateManyByQuery``), so no data is round-tripped through the
        client. An empty ``where`` would match every document and is refused.
        Raises :class:`~clappform.NotSupportedError` on a cluster that does
        not serve this RPC yet.
        """
        if not where:
            raise ValueError(
                "where={} matches every document; pass a filter that selects the "
                "documents to update"
            )
        self._client.data.update.update_many_by_query(
            collection=self.collection_id,
            query=_codec.encode_pipeline(dict(where)),
            set_values=_codec.encode_pipeline(dict(set_values)),
            location=self._location,
            timeout=timeout,
        )

    def replace_where(
        self,
        where: Mapping[str, Any],
        set_values: Mapping[str, Any],
        *,
        timeout: float | None = None,
    ) -> None:
        """Deprecated alias of :meth:`update_where`.

        Renamed because it sets fields (``$set``) rather than replacing
        documents. Removed before 6.0.0.
        """
        warnings.warn(
            "replace_where() is renamed to update_where(); replace_where() is "
            "removed before 6.0.0",
            DeprecationWarning,
            stacklevel=2,
        )
        self.update_where(where, set_values, timeout=timeout)

    def delete(
        self,
        *,
        where: Mapping[str, Any] | None = None,
        oids: Sequence[str] | None = None,
        timeout: float | None = None,
    ) -> None:
        """Delete documents by ``where`` filter or by explicit ``oids``.

        Exactly one of ``where`` / ``oids`` must be given. An empty ``oids``
        list deletes nothing and makes no call. To wipe the whole collection
        use :meth:`clear`, which is explicit by design so a full delete is
        never an accident of an empty filter. ``where=`` raises
        :class:`~clappform.NotSupportedError` on a cluster that does not serve
        ``DeleteManyByQuery`` yet.
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
            oid_list = list(oids)
            if not oid_list:
                return
            self._client.data.delete.delete_many_by_oids(
                collection=self.collection_id,
                oids=oid_list,
                location=self._location,
                timeout=timeout,
            )
            return
        # The XOR check above is the real guard; this only narrows for mypy.
        assert where is not None  # noqa: S101
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
    handle sends only the ``query`` field on ``AggregateStream``: no
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

        def _open() -> _Chunks:
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


def _require_key(records: list[Record], key: str, op: str) -> None:
    """Fail fast if any record lacks a value for the join key an update/upsert needs."""
    for index, record in enumerate(records):
        if key not in record:
            raise ValueError(f"{op} keyed on {key!r} but a row is missing that column")
        if _codec.is_missing(record[key]):
            raise ValueError(
                f"{op} keyed on {key!r} but row {index} has no value for it (null/NaN)"
            )
