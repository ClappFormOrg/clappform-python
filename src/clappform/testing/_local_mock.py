"""``LocalMock``: an in-process transport double for the Clappform client.

``LocalMock`` implements the :class:`~clappform._runtime.Caller` protocol, so
it plugs straight into ``Clappform(transport=LocalMock())`` and every generated
service method works against it with no network and no infrastructure.

It offers two layers:

* **Explicit stubs.** :meth:`LocalMock.on` registers a canned response, a
  handler callable, or (for streaming RPCs) an iterable of responses, keyed by
  the full gRPC method path. This works for *any* RPC in the client.
* **A seedable data-plane store.** :meth:`LocalMock.seed` loads records into a
  named collection, and built-in handlers for the core data RPCs read and
  mutate that store through the same JSON codec the real client uses:

  - ``AggregateStream`` (honours the ``$match``/``$project``/``$limit`` stages
    the DataFrame sugar compiles, and resolves a saved ``query`` through
    :meth:`seed_query`),
  - ``InsertSingle``/``InsertMany``, ``UpdateMany`` by ``_id``,
  - ``SyncManyByField`` (upsert on a business key),
  - ``UpdateManyByQuery`` (``replace_where``) and ``DeleteManyByQuery``,
  - ``DeleteManyByOids`` and ``Clear``.

  That is what lets the full DataFrame surface (read, filter, mutate, update,
  upsert, replace-where, delete) round-trip end-to-end in tests and in the
  guide snippets under ``docs/snippets/``. :meth:`seed_collection_slug` and
  :meth:`seed_query` register the Client API listings so slug/name resolution
  also runs without a server. An explicit stub for a method always wins over
  the built-in handler.

Every call is recorded on :attr:`LocalMock.calls` for assertions.
"""

from __future__ import annotations

import itertools
import json
from collections.abc import Callable, Iterable, Iterator
from dataclasses import dataclass
from typing import Any

from clappform import _codec
from clappform._errors import ClappformError
from clappform._runtime import CallKind

# A stub is a plain response, a callable taking the request, or (for streaming
# outputs) an iterable of responses / a callable returning one.
Handler = Callable[[Any], Any]


@dataclass(frozen=True)
class RecordedCall:
    """One invocation seen by the mock, captured for assertions."""

    kind: CallKind
    method: str
    request: Any
    timeout: float | None
    metadata: tuple[tuple[str, str], ...] | None
    location: str | None


class LocalMock:
    """Transport double: canned responses, a data store, and call recording."""

    def __init__(self) -> None:
        self.calls: list[RecordedCall] = []
        self._stubs: dict[str, Any] = {}
        self._store: dict[str, list[_codec.Record]] = {}
        self._queries: dict[str, str] = {}  # saved-query id -> backing collection
        self._query_listing: dict[str, str] = {}  # query name -> id (for GetAll)
        self._collection_listing: dict[str, str] = {}  # collection slug -> id
        self._oids = itertools.count(1)
        self._closed = False

    # -- configuration ---------------------------------------------------

    def on(self, method: str, response: Any) -> LocalMock:
        """Register a canned ``response`` for a full gRPC ``method`` path.

        ``response`` may be a response message, a callable ``handler(request)``
        returning one, or (for a streaming-output RPC) an iterable of
        response messages (or a callable returning such an iterable). Returns
        ``self`` so registrations chain. Registering the same method twice
        replaces the earlier stub.
        """
        self._stubs[method] = response
        return self

    def seed(self, collection: str, records: Iterable[_codec.Record]) -> LocalMock:
        """Load ``records`` into ``collection``'s in-memory store (replacing it).

        Each record without an ``_id`` is given a synthetic one so update and
        delete round-trips have a stable key. Returns ``self`` for chaining.
        """
        stored: list[_codec.Record] = []
        for record in records:
            row = dict(record)
            if "_id" not in row or row["_id"] is None:
                row["_id"] = self._next_oid()
            stored.append(row)
        self._store[collection] = stored
        return self

    def seed_query(self, ref: str, *, collection: str, id: str | None = None) -> LocalMock:
        """Register a saved query ``ref`` that reads from ``collection``.

        Lets ``cf.data.query(ref).read()`` work end-to-end: a name ``ref``
        resolves through a canned ``QueryManagement/GetAll`` (so the client's
        name->UUID lookup finds it), and the AggregateStream handler serves the
        backing ``collection``'s rows for the resulting query id. A ``ref`` that
        is already a UUID skips resolution and is used as the id directly.
        ``id`` overrides the generated UUID. Returns ``self`` for chaining.
        """
        from clappform._resolve import is_uuid

        query_id = id or (ref if is_uuid(ref) else self._next_oid())
        self._queries[query_id] = collection
        if not is_uuid(ref):
            self._register_query_listing(ref, query_id)
        return self

    def _register_query_listing(self, name: str, query_id: str) -> None:
        """Add ``name``->``query_id`` to the canned query GetAll listing."""
        from clappform.gen.clappform.client.v1.query import query_pb2
        from clappform.gen.clappform.v1.commons import commons_pb2

        self._query_listing[name] = query_id

        def _get_all(_request: Any) -> Any:
            queries = [
                query_pb2.Query(id=qid, name=qname) for qname, qid in self._query_listing.items()
            ]
            return query_pb2.Queries(
                queries=queries,
                pagination=commons_pb2.Pagination(page=1, pages=1, total=len(queries)),
            )

        self.on("/clappform.client.v1.query.QueryManagement/GetAll", _get_all)

    def seed_collection_slug(self, slug: str, *, id: str) -> LocalMock:
        """Register a collection ``slug``->``id`` mapping for slug resolution.

        Lets ``cf.data.collection(slug).read()`` resolve the slug to ``id``
        through a canned ``CollectionManagement/GetAll`` before reading the
        store seeded under ``id`` (via :meth:`seed`). Returns ``self``.
        """
        from clappform.gen.clappform.client.v1.collection import collection_pb2
        from clappform.gen.clappform.v1.commons import commons_pb2

        self._collection_listing[slug] = id

        def _get_all(_request: Any) -> Any:
            collections = [
                collection_pb2.Collection(id=cid, slug=cslug)
                for cslug, cid in self._collection_listing.items()
            ]
            return collection_pb2.Collections(
                collections=collections,
                pagination=commons_pb2.Pagination(page=1, pages=1, total=len(collections)),
            )

        self.on("/clappform.client.v1.collection.CollectionManagement/GetAll", _get_all)
        return self

    def records(self, collection: str) -> list[_codec.Record]:
        """A copy of the records currently stored for ``collection``."""
        return [dict(row) for row in self._store.get(collection, [])]

    def reset(self) -> None:
        """Clear recorded calls, stubs and the data store."""
        self.calls.clear()
        self._stubs.clear()
        self._store.clear()
        self._queries.clear()
        self._query_listing.clear()
        self._collection_listing.clear()

    def close(self) -> None:
        """Mark the mock closed, matching the transport's teardown contract."""
        self._closed = True

    # -- Caller protocol -------------------------------------------------

    def invoke(
        self,
        kind: CallKind,
        method: str,
        request: Any,
        request_cls: type,
        response_cls: type,
        *,
        timeout: float | None = None,
        metadata: tuple[tuple[str, str], ...] | None = None,
        location: str | None = None,
    ) -> Any:
        if self._closed:
            raise ClappformError("client is closed", method=method)
        materialised = list(request) if kind.startswith("stream") else request
        self.calls.append(RecordedCall(kind, method, materialised, timeout, metadata, location))

        if method in self._stubs:
            return self._dispatch_stub(kind, method, materialised, response_cls)

        handler = _DATA_HANDLERS.get(method)
        if handler is not None:
            return handler(self, kind, materialised, response_cls)

        raise ClappformError(
            f"LocalMock has no response for {method!r}; register one with "
            f".on({method!r}, ...) or seed a collection for the data RPCs",
            method=method,
        )

    def _dispatch_stub(self, kind: CallKind, method: str, request: Any, response_cls: type) -> Any:
        stub = self._stubs[method]
        streaming_out = kind.endswith("_stream")
        is_handler = callable(stub) and not isinstance(stub, response_cls)
        result = stub(request) if is_handler else stub
        if streaming_out:
            if isinstance(result, (str, bytes)) or not isinstance(result, Iterable):
                raise ClappformError(
                    f"stub for streaming method {method!r} must be an iterable of "
                    f"responses, got {type(result).__name__}",
                    method=method,
                )
            return iter(result)
        if isinstance(result, Iterator):
            # A stub returned an iterator for a unary-output RPC: take the
            # first item so a single canned response still works.
            return next(result)
        return result

    # -- data-plane store helpers ---------------------------------------

    def _next_oid(self) -> str:
        return f"mock-oid-{next(self._oids)}"

    def _collection_of(self, request: Any) -> str:
        collection = getattr(request, "collection", "")
        if not collection:
            raise ClappformError("LocalMock data handlers require a 'collection' on the request")
        return collection


def _aggregate_target(mock: LocalMock, request: Any) -> str:
    """The collection an AggregateStream request reads from.

    A ``query`` request names a saved query, which resolves to its backing
    collection through the ``seed_query`` registry; otherwise the request
    carries the collection directly.
    """
    query = getattr(request, "query", "")
    if query:
        collection = mock._queries.get(query)
        if collection is None:
            raise ClappformError(
                f"LocalMock has no saved query {query!r}; register one with "
                f".seed_query({query!r}, collection=...)"
            )
        return collection
    return mock._collection_of(request)


def _apply_pipeline(rows: list[_codec.Record], pipeline: bytes) -> list[_codec.Record]:
    """Apply the ``$match``/``$project``/``$limit`` stages the sugar emits.

    Only the stages ``read(where=, fields=, limit=)`` compiles are honoured,
    enough to test the client sugar without reimplementing an aggregation
    engine. ``$match`` supports equality on top-level fields; other operators
    and stages are passed over so a caller-supplied pipeline still streams the
    whole collection rather than erroring.
    """
    if not pipeline:
        return list(rows)
    result = list(rows)
    for stage in json.loads(pipeline):
        if not isinstance(stage, dict) or len(stage) != 1:
            continue
        ((op, arg),) = stage.items()
        if op == "$match" and isinstance(arg, dict):
            result = [
                row
                for row in result
                if all(not isinstance(v, dict) and row.get(k) == v for k, v in arg.items())
            ]
        elif op == "$project" and isinstance(arg, dict):
            keep = {k for k, v in arg.items() if v}
            keep.add("_id")  # _id survives projection unless explicitly excluded
            result = [{k: v for k, v in row.items() if k in keep} for row in result]
        elif op == "$limit" and isinstance(arg, int):
            result = result[:arg]
    return result


def _handle_aggregate_stream(
    mock: LocalMock, kind: CallKind, request: Any, response_cls: type
) -> Iterator[Any]:
    """Serve seeded records as AggregateStream chunks.

    Resolves the target collection from either the ``collection`` field or a
    saved ``query`` (registered via :meth:`LocalMock.seed_query`), then applies
    the ``$match``/``$project``/``$limit`` stages the DataFrame sugar compiles,
    so a filtered/projected/limited ``read()`` round-trips against the store.
    Pipeline stages the sugar never emits are ignored by this double.
    """
    collection = _aggregate_target(mock, request)
    records = _apply_pipeline(mock._store.get(collection, []), request.pipeline)
    total = len(records)
    batch_size = getattr(request, "batch_size", 0) or _codec.DEFAULT_CHUNK_ROWS

    def _chunks() -> Iterator[Any]:
        if not records:
            yield response_cls(data=b"[]", total=0, total_sent=0)
            return
        sent = 0
        for start in range(0, total, batch_size):
            chunk = records[start : start + batch_size]
            sent += len(chunk)
            yield response_cls(
                data=_codec.records_to_bytes(chunk),
                total=total,
                total_sent=sent,
            )

    return _chunks()


def _handle_insert(mock: LocalMock, kind: CallKind, request: Any, response_cls: type) -> Any:
    """Append decoded records to the store, assigning ids; report counts.

    Handles ``InsertSingle`` (unary-unary) and ``InsertMany`` (stream-stream).
    For the stream case the recorded request is a list of ``InsertRequest`` and
    one ``InsertResponse`` is yielded per request message, matching the real
    bidi transport; the unary case returns a single response.
    """
    requests = request if isinstance(request, list) else [request]

    def _apply(req: Any) -> Any:
        collection = mock._collection_of(req)
        store = mock._store.setdefault(collection, [])
        oids: list[str] = []
        for record in _codec.bytes_to_records(req.data):
            row = dict(record)
            if "_id" not in row or row["_id"] is None:
                row["_id"] = mock._next_oid()
            store.append(row)
            oids.append(str(row["_id"]))
        return response_cls(processed_count=len(oids), oids=oids)

    if kind.endswith("_stream"):
        return iter([_apply(req) for req in requests])
    return _apply(requests[0])


def _build_response(response_cls: type, **fields: Any) -> Any:
    """Construct a response, keeping only fields the message actually declares.

    Data RPCs vary in their response shape (some return a data-bearing message,
    some a plain ``Message{message}``); this way one handler serves either
    without hardcoding a schema the proto may not have.
    """
    declared = {f.name for f in response_cls.DESCRIPTOR.fields}  # type: ignore[attr-defined]
    kept = {name: value for name, value in fields.items() if name in declared}
    return response_cls(**kept)


def _handle_update_many(mock: LocalMock, kind: CallKind, request: Any, response_cls: type) -> Any:
    """Apply field updates to stored rows matched by ``_id``.

    ``UpdateMany`` is stream-unary, so ``request`` is a list of update messages;
    every message's records are applied in order.
    """
    requests = request if isinstance(request, list) else [request]
    collection = ""
    for req in requests:
        collection = mock._collection_of(req)
        store = mock._store.setdefault(collection, [])
        by_id = {str(row.get("_id")): row for row in store}
        for record in _codec.bytes_to_records(req.data):
            target = by_id.get(str(record.get("_id")))
            if target is not None:
                target.update({k: v for k, v in record.items() if k != "_id"})
    store = mock._store.get(collection, [])
    return _build_response(
        response_cls,
        data=_codec.records_to_bytes(store),
        collection=collection,
        message=f"updated {collection!r}",
    )


def _handle_delete_oids(mock: LocalMock, kind: CallKind, request: Any, response_cls: type) -> Any:
    """Remove stored rows whose ``_id`` is in the request's oids."""
    collection = mock._collection_of(request)
    store = mock._store.setdefault(collection, [])
    targets = {str(oid) for oid in request.oids}
    kept = [row for row in store if str(row.get("_id")) not in targets]
    removed = len(store) - len(kept)
    mock._store[collection] = kept
    return _build_response(
        response_cls,
        total=len(kept),
        total_sent=removed,
        message=f"deleted {removed} rows",
    )


def _handle_sync_by_field(
    mock: LocalMock, kind: CallKind, request: Any, response_cls: type
) -> Any:
    """Upsert rows keyed on ``field_name``: update matches, insert the rest.

    ``SyncManyByField`` is stream-unary, so ``request`` is a list of sync
    messages; each message's records are matched against the store by their
    ``field_name`` value.
    """
    requests = request if isinstance(request, list) else [request]
    collection = ""
    for req in requests:
        collection = mock._collection_of(req)
        field = req.field_name
        store = mock._store.setdefault(collection, [])
        by_key = {row.get(field): row for row in store}
        for record in _codec.bytes_to_records(req.data):
            key = record.get(field)
            target = by_key.get(key)
            if target is not None:
                target.update(record)
            else:
                row = dict(record)
                if "_id" not in row or row["_id"] is None:
                    row["_id"] = mock._next_oid()
                store.append(row)
                by_key[key] = row
    store = mock._store.get(collection, [])
    return _build_response(
        response_cls,
        data=_codec.records_to_bytes(store),
        collection=collection,
        message=f"synced {collection!r}",
    )


def _handle_update_by_query(
    mock: LocalMock, kind: CallKind, request: Any, response_cls: type
) -> Any:
    """Apply ``set_values`` to every stored row matching the query filter.

    Backs ``replace_where``. The query and set-values are JSON as the client
    sends them; only equality on top-level fields is matched, matching the
    aggregate handler's ``$match`` support.
    """
    collection = mock._collection_of(request)
    store = mock._store.setdefault(collection, [])
    query = json.loads(request.query) if request.query else {}
    set_values = json.loads(request.set_values) if request.set_values else {}
    matched = 0
    for row in store:
        if all(row.get(k) == v for k, v in query.items()):
            row.update(set_values)
            matched += 1
    return _build_response(
        response_cls,
        data=_codec.records_to_bytes(store),
        collection=collection,
        total=len(store),
        total_sent=matched,
        message=f"updated {matched} rows in {collection!r}",
    )


def _handle_delete_by_query(
    mock: LocalMock, kind: CallKind, request: Any, response_cls: type
) -> Any:
    """Remove stored rows matching the query filter (equality on top-level)."""
    collection = mock._collection_of(request)
    store = mock._store.setdefault(collection, [])
    query = json.loads(request.query) if request.query else {}
    kept = [row for row in store if not all(row.get(k) == v for k, v in query.items())]
    removed = len(store) - len(kept)
    mock._store[collection] = kept
    return _build_response(
        response_cls,
        total=len(kept),
        total_sent=removed,
        message=f"deleted {removed} rows",
    )


def _handle_clear(mock: LocalMock, kind: CallKind, request: Any, response_cls: type) -> Any:
    """Empty a collection's store."""
    collection = mock._collection_of(request)
    mock._store[collection] = []
    return _build_response(response_cls, message=f"cleared {collection!r}")


# Full method path -> built-in data-plane handler. Explicit .on() stubs win.
_DATA_HANDLERS: dict[str, Callable[[LocalMock, CallKind, Any, type], Any]] = {
    "/clappform.data.v1.aggregate.AggregateManagement/AggregateStream": _handle_aggregate_stream,
    "/clappform.data.v1.insert.InsertManagement/InsertSingle": _handle_insert,
    "/clappform.data.v1.insert.InsertManagement/InsertMany": _handle_insert,
    "/clappform.data.v1.update.UpdateManagement/UpdateMany": _handle_update_many,
    "/clappform.data.v1.update.UpdateManagement/UpdateManyByQuery": _handle_update_by_query,
    "/clappform.data.v1.sync.SyncManagement/SyncManyByField": _handle_sync_by_field,
    "/clappform.data.v1.delete.DeleteManagement/DeleteManyByOids": _handle_delete_oids,
    "/clappform.data.v1.delete.DeleteManagement/DeleteManyByQuery": _handle_delete_by_query,
    "/clappform.data.v1.delete.DeleteManagement/Clear": _handle_clear,
}
