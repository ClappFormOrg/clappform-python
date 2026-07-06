"""In-process gRPC servers used to exercise the full client stack.

These servicers implement the generated gRPC service base classes with just
enough canned logic to drive real client flows — pagination, DataFrame
round-trips, slug resolution, streaming, and retries — over a genuine
127.0.0.1 channel. Because the client talks to them through its production
transport, every test that uses them covers interceptors (metadata), the
codec, retry configuration, and error translation, not just the wrapper layer.

Nothing here reaches the network beyond loopback. A single :class:`FakeCluster`
bundles every servicer a test might need behind one address, so a client can
be pointed at it with ``endpoints={...}`` for all families.
"""

from __future__ import annotations

import threading
from collections.abc import Iterator
from concurrent import futures
from dataclasses import dataclass, field
from typing import Any

import grpc

from clappform import _codec
from clappform.gen.clappform.client.v1.collection import (
    collection_pb2,
    collection_pb2_grpc,
)
from clappform.gen.clappform.data.v1.aggregate import aggregate_pb2, aggregate_pb2_grpc
from clappform.gen.clappform.data.v1.insert import insert_pb2, insert_pb2_grpc
from clappform.gen.clappform.v1.commons import commons_pb2


def location_of(context: grpc.ServicerContext) -> str:
    """Read the tenant ``location`` header the client is required to send."""
    return dict(context.invocation_metadata()).get("location", "")


@dataclass
class CollectionStore:
    """State for a single collection keyed by UUID: its slug and its rows.

    ``fail_unavailable`` makes the first N reads of this collection abort with
    ``UNAVAILABLE`` before succeeding, so retry behaviour can be driven without
    depending on wall-clock timing.
    """

    slug: str
    rows: list[dict[str, Any]] = field(default_factory=list)
    fail_unavailable: int = 0


class CollectionListServicer(collection_pb2_grpc.CollectionManagementServicer):
    """Serves the paginated listing the slug resolver walks.

    ``GetAll`` pages a fixed number of collections per request so the client's
    ``iter_get_all`` auto-pagination is genuinely exercised — more than one
    page, terminating when ``page >= pages``. The listing is location-scoped:
    a tenant only sees the collections registered for it, which is what lets
    the per-location resolver cache be tested end-to-end.
    """

    def __init__(self, page_size: int = 2) -> None:
        self.page_size = page_size
        # location -> {uuid: CollectionStore}
        self._by_location: dict[str, dict[str, CollectionStore]] = {}
        self.get_all_calls = 0

    def register(self, location: str, uuid: str, store: CollectionStore) -> None:
        self._by_location.setdefault(location, {})[uuid] = store

    def store_for(self, location: str, uuid: str) -> CollectionStore | None:
        return self._by_location.get(location, {}).get(uuid)

    def all_for(self, location: str) -> dict[str, CollectionStore]:
        return self._by_location.get(location, {})

    def GetAll(self, request, context):  # noqa: N802 - gRPC servicer name
        self.get_all_calls += 1
        location = location_of(context)
        collections = [
            collection_pb2.Collection(id=uuid, slug=store.slug)
            for uuid, store in self.all_for(location).items()
        ]
        page = request.page or 1
        pages = max(1, (len(collections) + self.page_size - 1) // self.page_size)
        start = (page - 1) * self.page_size
        window = collections[start : start + self.page_size]
        return collection_pb2.Collections(
            collections=window,
            pagination=commons_pb2.Pagination(
                page=page, pages=pages, total=len(collections)
            ),
        )


class AggregateReadServicer(aggregate_pb2_grpc.AggregateManagementServicer):
    """Streams a collection's rows back as JSON-encoded ``AggregateResponse``s.

    Rows are looked up by the request's ``collection`` UUID (or, for saved
    queries, resolved by the ``query`` UUID to a backing collection), encoded
    through the real codec, and chunked so the streaming path and the
    ReadResult batching are both driven. A collection whose store carries
    ``fail_unavailable=N`` aborts with ``UNAVAILABLE`` on its first N reads
    before succeeding, which is how retry behaviour is tested without touching
    timing. ``attempts`` records reads per UUID so tests can assert how many
    attempts the retry policy made.
    """

    def __init__(self, collections: CollectionListServicer) -> None:
        self._collections = collections
        self._query_to_collection: dict[str, str] = {}
        self.attempts: dict[str, int] = {}
        self._lock = threading.Lock()

    def register_query(self, query_uuid: str, collection_uuid: str) -> None:
        self._query_to_collection[query_uuid] = collection_uuid

    def _store_for(self, location: str, request) -> CollectionStore | None:
        uuid = request.collection
        if request.query:
            uuid = self._query_to_collection.get(request.query, "")
        return self._collections.store_for(location, uuid)

    def AggregateStream(self, request, context):  # noqa: N802
        location = location_of(context)
        store = self._store_for(location, request)
        uuid = request.query or request.collection
        with self._lock:
            seen = self.attempts.get(uuid, 0) + 1
            self.attempts[uuid] = seen
        if store is not None and seen <= store.fail_unavailable:
            context.abort(grpc.StatusCode.UNAVAILABLE, "cluster warming up")
        rows = list(store.rows) if store is not None else []
        if not rows:
            yield aggregate_pb2.AggregateResponse(data=b"[]", total=0)
            return
        # One record per chunk so the ReadResult batching has multiple chunks.
        for row in rows:
            yield aggregate_pb2.AggregateResponse(
                data=_codec.records_to_bytes([row]), total=len(rows)
            )


class InsertServicer(insert_pb2_grpc.InsertManagementServicer):
    """Client-streaming insert that appends decoded rows into a store.

    ``InsertMany`` consumes the request iterator (each carrying a JSON chunk),
    appends the decoded records to the matching collection, and returns one
    ``InsertResponse`` per request with the rows processed and assigned oids —
    enough for the DataFrame ``append`` round-trip and for asserting the
    ``location`` header arrives on a client-streaming call.
    """

    def __init__(self, collections: CollectionListServicer) -> None:
        self._collections = collections
        self.seen_location: str | None = None
        self._counter = 0
        self._lock = threading.Lock()

    def _store(self, location: str, uuid: str) -> CollectionStore | None:
        return self._collections.store_for(location, uuid)

    def InsertMany(self, request_iterator, context):  # noqa: N802
        self.seen_location = location_of(context)
        for request in request_iterator:
            records = _codec.bytes_to_records(request.data)
            store = self._store(self.seen_location, request.collection)
            oids = []
            for record in records:
                with self._lock:
                    self._counter += 1
                    oid = f"oid-{self._counter}"
                record = {"_id": oid, **record}
                if store is not None:
                    store.rows.append(record)
                oids.append(oid)
            yield insert_pb2.InsertResponse(
                processed_count=len(records), oids=oids
            )


@dataclass
class FakeCluster:
    """A started in-process gRPC server exposing every fake servicer.

    Every API family (``data``, ``client``, ...) is pointed at this one
    address, so a client built with ``endpoints=cluster.endpoints`` routes all
    calls here. ``address`` is loopback-only.
    """

    server: grpc.Server
    address: str
    collections: CollectionListServicer
    aggregate: AggregateReadServicer
    insert: InsertServicer

    @property
    def endpoints(self) -> dict[str, str]:
        return {family: self.address for family in ("data", "client", "auth", "notifier")}

    def register_collection(
        self,
        *,
        location: str,
        uuid: str,
        slug: str,
        rows: list[dict[str, Any]],
        fail_unavailable: int = 0,
    ) -> None:
        self.collections.register(
            location,
            uuid,
            CollectionStore(slug=slug, rows=rows, fail_unavailable=fail_unavailable),
        )

    def register_query(
        self, *, query_uuid: str, collection_uuid: str
    ) -> None:
        self.aggregate.register_query(query_uuid, collection_uuid)

    def stop(self) -> None:
        self.server.stop(grace=None)


def start_fake_cluster(page_size: int = 2) -> FakeCluster:
    """Build, wire, and start a :class:`FakeCluster` on a free loopback port."""
    collections = CollectionListServicer(page_size=page_size)
    aggregate = AggregateReadServicer(collections)
    insert = InsertServicer(collections)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=8))
    collection_pb2_grpc.add_CollectionManagementServicer_to_server(collections, server)
    aggregate_pb2_grpc.add_AggregateManagementServicer_to_server(aggregate, server)
    insert_pb2_grpc.add_InsertManagementServicer_to_server(insert, server)
    port = server.add_insecure_port("127.0.0.1:0")
    server.start()
    return FakeCluster(
        server=server,
        address=f"127.0.0.1:{port}",
        collections=collections,
        aggregate=aggregate,
        insert=insert,
    )


def drain(stream: Iterator[Any]) -> list[Any]:
    """Materialise a streaming response, for tests that assert on all chunks."""
    return list(stream)
