"""Slug/name -> UUID resolution for collection and query handles.

Exercises the resolver through the real client and ``LocalMock``: UUIDs pass
through untouched, slugs resolve via the Client API and cache per location, a
stale cached UUID re-resolves once, and an unknown slug raises ``NotFoundError``.
"""

import pytest

from clappform import Clappform, NotFoundError
from clappform._resolve import is_uuid
from clappform.testing import LocalMock

CID = "1c9a7f3e-0000-4000-8000-000000000001"
QID = "8f14e45f-ceea-467f-a34e-95b7f7f7a9d1"
COLLECTION_GET_ALL = "/clappform.client.v1.collection.CollectionManagement/GetAll"
QUERY_GET_ALL = "/clappform.client.v1.query.QueryManagement/GetAll"
AGG = "/clappform.data.v1.aggregate.AggregateManagement/AggregateStream"


@pytest.fixture
def cf():
    mock = LocalMock()
    client = Clappform("acme", "qa", api_key="k", transport=mock)
    yield client, mock
    client.close()


# -- UUID detection ------------------------------------------------------


@pytest.mark.parametrize(
    "value,expected",
    [
        (CID, True),
        ("{1c9a7f3e-0000-4000-8000-000000000001}", True),
        ("sales_orders", False),
        ("monthly-revenue", False),  # a hyphenated slug is NOT a uuid
        ("", False),
    ],
)
def test_is_uuid(value, expected) -> None:
    assert is_uuid(value) is expected


# -- collection resolution -----------------------------------------------


def test_uuid_ref_is_used_without_lookup(cf) -> None:
    client, mock = cf
    mock.seed(CID, [{"n": 1}])
    df = client.data.collection(CID).read()
    assert len(df) == 1
    # No collection listing was consulted; the UUID went straight through.
    assert not any(c.method == COLLECTION_GET_ALL for c in mock.calls)


def test_slug_resolves_and_reads(cf) -> None:
    client, mock = cf
    mock.seed(CID, [{"n": 1}, {"n": 2}])
    mock.seed_collection_slug("sales_orders", id=CID)
    col = client.data.collection("sales_orders")
    assert len(col.read()) == 2
    assert col.collection_id == CID


def test_slug_resolution_is_cached_across_calls(cf) -> None:
    client, mock = cf
    mock.seed(CID, [{"n": 1}])
    mock.seed_collection_slug("sales_orders", id=CID)
    col = client.data.collection("sales_orders")
    col.read()
    col.read()
    col.read()
    lookups = [c for c in mock.calls if c.method == COLLECTION_GET_ALL]
    assert len(lookups) == 1  # one extra RPC per process, not per call


def test_unknown_slug_raises_not_found_naming_slug_and_location(cf) -> None:
    client, mock = cf
    mock.seed_collection_slug("exists", id=CID)  # registers the listing, not our slug
    with pytest.raises(NotFoundError, match="ghost") as exc:
        client.data.collection("ghost").read()
    assert "acme" in str(exc.value)  # the location searched


def test_stale_cached_uuid_reresolves_once(cf) -> None:
    """A cached slug->UUID that NOT_FOUNDs must re-resolve before surfacing."""
    client, mock = cf
    old_id, new_id = CID, "2222aaaa-0000-4000-8000-000000000002"
    mock.seed(new_id, [{"n": 42}])
    mock.seed_collection_slug("sales_orders", id=old_id)

    # First read resolves "sales_orders" -> old_id and caches it, but old_id
    # has no store and (per this stub) reads NOT_FOUND. Re-point the slug at the
    # live collection so the re-resolution finds it.

    def _agg(request):
        if request.collection == old_id:
            raise NotFoundError("collection gone", location="acme")
        # serve new_id's rows as a single chunk
        from clappform import _codec
        from clappform.gen.clappform.data.v1.aggregate import aggregate_pb2

        rows = mock.records(new_id)
        return [aggregate_pb2.AggregateResponse(data=_codec.records_to_bytes(rows))]

    mock.on(AGG, _agg)

    col = client.data.collection("sales_orders")
    assert col.collection_id == old_id  # resolves + caches old_id
    mock.seed_collection_slug("sales_orders", id=new_id)  # slug remapped

    df = col.read()  # first attempt hits old_id -> NOT_FOUND -> re-resolve
    assert list(df["n"]) == [42]
    assert col.collection_id == new_id


def test_not_found_after_first_chunk_is_not_retried(cf) -> None:
    """A NOT_FOUND once rows have streamed surfaces raw, with no silent replay.

    Re-resolving mid-stream would re-deliver already-yielded rows, so the retry
    is intentionally limited to a NOT_FOUND on the probing first chunk.
    """
    client, mock = cf
    from clappform import _codec
    from clappform.gen.clappform.data.v1.aggregate import aggregate_pb2

    mock.seed_collection_slug("orders", id=CID)

    def _agg(_request):
        def _stream():
            yield aggregate_pb2.AggregateResponse(
                data=_codec.records_to_bytes([{"n": 1}])
            )
            raise NotFoundError("collection vanished mid-scan", location="acme")

        return _stream()

    mock.on(AGG, _agg)
    with pytest.raises(NotFoundError, match="mid-scan"):
        client.data.collection("orders").read()


def test_reads_isolate_cache_per_location(cf) -> None:
    """A slug resolved for one tenant is not reused for another (per-location)."""
    client, mock = cf
    other = client.with_location("umbrella")
    a_id, b_id = CID, "3333bbbb-0000-4000-8000-000000000003"
    mock.seed(a_id, [{"who": "acme"}])
    mock.seed(b_id, [{"who": "umbrella"}])

    def _get_all(request):
        from clappform.gen.clappform.client.v1.collection import collection_pb2
        from clappform.gen.clappform.v1.commons import commons_pb2

        # the listing depends on which tenant asks (location metadata)
        loc = _location_of(mock)
        cid = a_id if loc == "acme" else b_id
        return collection_pb2.Collections(
            collections=[collection_pb2.Collection(id=cid, slug="orders")],
            pagination=commons_pb2.Pagination(page=1, pages=1, total=1),
        )

    mock.on(COLLECTION_GET_ALL, _get_all)

    assert client.data.collection("orders").collection_id == a_id
    assert other.data.collection("orders").collection_id == b_id


def _location_of(mock: LocalMock) -> str:
    for call in reversed(mock.calls):
        if call.method == COLLECTION_GET_ALL:
            return call.location
    raise AssertionError("no listing call recorded")


# -- saved-query resolution ----------------------------------------------


def test_query_by_uuid_reads_without_lookup(cf) -> None:
    client, mock = cf
    mock.seed(CID, [{"r": 1}, {"r": 2}])
    mock.seed_query(QID, collection=CID, id=QID)
    df = client.data.query(QID).read()
    assert len(df) == 2


def test_query_by_name_resolves_and_reads(cf) -> None:
    client, mock = cf
    mock.seed(CID, [{"revenue": 100}])
    mock.seed_query("monthly-revenue", collection=CID, id=QID)
    q = client.data.query("monthly-revenue")
    df = q.read()
    assert list(df["revenue"]) == [100]
    assert q.query_id == QID


def test_query_sends_only_query_field_no_collection(cf) -> None:
    client, mock = cf
    mock.seed(CID, [{"r": 1}])
    mock.seed_query("monthly-revenue", collection=CID, id=QID)
    client.data.query("monthly-revenue").read()
    (agg_call,) = [c for c in mock.calls if c.method == AGG]
    assert agg_call.request.query == QID
    assert not agg_call.request.collection  # a saved query carries its own


def test_unknown_query_name_raises(cf) -> None:
    client, mock = cf
    mock.seed_query("exists", collection=CID, id=QID)
    with pytest.raises(NotFoundError, match="phantom"):
        client.data.query("phantom").read()


def test_query_name_resolution_is_cached_across_handles(cf) -> None:
    client, mock = cf
    mock.seed(CID, [{"r": 1}])
    mock.seed_query("monthly-revenue", collection=CID, id=QID)
    # Fresh handles each round: the resolver (not the handle) must serve the
    # second lookup from cache, so only one listing RPC hits the wire.
    client.data.query("monthly-revenue").read()
    client.data.query("monthly-revenue").read()
    client.data.query("monthly-revenue").read()
    lookups = [c for c in mock.calls if c.method == QUERY_GET_ALL]
    assert len(lookups) == 1  # name->UUID resolved once per location, then cached


def test_stale_cached_query_uuid_reresolves_once(cf) -> None:
    """A cached name->UUID that NOT_FOUNDs must re-resolve before surfacing.

    Mirrors the collection stale-cache path for QueryHandle: the first read
    resolves the name to a now-defunct UUID; on the NOT_FOUND probing the first
    chunk the handle invalidates the cache, re-resolves, and retries once.
    """
    client, mock = cf
    from clappform import _codec
    from clappform.gen.clappform.data.v1.aggregate import aggregate_pb2

    old_id, new_id = QID, "4444cccc-0000-4000-8000-000000000004"
    mock.seed(CID, [{"revenue": 100}])
    mock.seed_query("monthly-revenue", collection=CID, id=old_id)

    def _agg(request):
        if request.query == old_id:
            raise NotFoundError("query gone", location="acme")
        rows = mock.records(CID)
        return [aggregate_pb2.AggregateResponse(data=_codec.records_to_bytes(rows))]

    mock.on(AGG, _agg)

    q = client.data.query("monthly-revenue")
    assert q.query_id == old_id  # resolves + caches old_id
    mock.seed_query("monthly-revenue", collection=CID, id=new_id)  # name remapped

    df = q.read()  # first attempt hits old_id -> NOT_FOUND -> re-resolve
    assert list(df["revenue"]) == [100]
    assert q.query_id == new_id


def test_query_not_found_after_first_chunk_is_not_retried(cf) -> None:
    """A NOT_FOUND once rows have streamed surfaces raw, with no silent replay.

    The QueryHandle counterpart to the collection mid-stream test: re-resolving
    after rows were yielded would re-deliver them, so the retry is limited to a
    NOT_FOUND on the probing first chunk.
    """
    client, mock = cf
    from clappform import _codec
    from clappform.gen.clappform.data.v1.aggregate import aggregate_pb2

    mock.seed(CID, [{"r": 1}])
    mock.seed_query("monthly-revenue", collection=CID, id=QID)

    def _agg(_request):
        def _stream():
            yield aggregate_pb2.AggregateResponse(
                data=_codec.records_to_bytes([{"r": 1}])
            )
            raise NotFoundError("query vanished mid-scan", location="acme")

        return _stream()

    mock.on(AGG, _agg)
    with pytest.raises(NotFoundError, match="mid-scan"):
        client.data.query("monthly-revenue").read()
