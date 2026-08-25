"""Full-stack coverage through in-process gRPC servers.

Where ``test_transport_grpc.py`` proves the transport primitives (metadata,
deadlines, error translation, streaming), this module drives the higher-level
flows (pagination, DataFrame round-trips, slug resolution and its cache, and
retry-on-UNAVAILABLE) against real generated servicers over a loopback
channel. Every assertion therefore exercises the whole client stack:
interceptors, codec, retry service config, and error translation together, not
a mocked transport.

The fakes live in ``tests/_grpc_fakes.py``; each test points a ``Clappform``
at one :class:`FakeCluster` address for all API families.
"""

from __future__ import annotations

import pytest
from _grpc_fakes import start_fake_cluster

from clappform import Clappform, NotFoundError, TransientError
from clappform._transport import RetryPolicy

CID = "1c9a7f3e-0000-4000-8000-000000000001"
CID2 = "2222aaaa-0000-4000-8000-000000000002"
QID = "8f14e45f-ceea-467f-a34e-95b7f7f7a9d1"


@pytest.fixture
def cluster():
    fake = start_fake_cluster()
    yield fake
    fake.stop()


def _client(cluster, *, retries: RetryPolicy | None = None, **kwargs) -> Clappform:
    return Clappform(
        "acme",
        "qa",
        api_key="test-key",
        endpoints=cluster.endpoints,
        insecure=True,
        timeout=5.0,
        retries=retries,
        **kwargs,
    )


# -- location metadata on a client-streaming call ------------------------


def test_client_streaming_carries_location_metadata(cluster) -> None:
    """The location header must ride client-streaming RPCs, not only unary ones."""
    import pandas as pd

    cluster.register_collection(location="acme", uuid=CID, slug="orders", rows=[])
    with _client(cluster) as cf:
        written = cf.data.collection(CID).append(pd.DataFrame([{"amount": 10}]))
    assert written == 1
    assert cluster.insert.seen_location == "acme"


def test_client_streaming_location_override_wins(cluster) -> None:
    import pandas as pd

    cluster.register_collection(location="umbrella", uuid=CID, slug="orders", rows=[])
    with _client(cluster) as cf:
        cf.with_location("umbrella").data.collection(CID).append(
            pd.DataFrame([{"amount": 5}])
        )
    assert cluster.insert.seen_location == "umbrella"


# -- pagination iterator over the real wire ------------------------------


def test_iter_get_all_walks_every_page(cluster) -> None:
    """The auto-pagination iterator must follow ``Pagination`` across pages.

    The fake serves 2 collections per page, so five collections span three
    pages; the iterator must yield all five and stop when page == pages.
    """
    slugs = [f"c{i}" for i in range(5)]
    for i, slug in enumerate(slugs):
        cluster.register_collection(
            location="acme", uuid=f"{i}0000000-0000-4000-8000-000000000000", slug=slug, rows=[]
        )
    with _client(cluster) as cf:
        seen = [c.slug for c in cf.client.collection.iter_get_all()]
    assert sorted(seen) == sorted(slugs)
    assert cluster.collections.get_all_calls == 3  # ceil(5 / 2) pages


# -- DataFrame round-trip through append + read --------------------------


def test_dataframe_round_trip_append_then_read(cluster) -> None:
    """Rows appended via InsertMany read back byte-identical through AggregateStream."""
    import pandas as pd

    cluster.register_collection(location="acme", uuid=CID, slug="orders", rows=[])
    with _client(cluster) as cf:
        col = cf.data.collection(CID)
        col.append(pd.DataFrame([{"region": "eu", "amount": 10}, {"region": "us", "amount": 20}]))
        df = col.read()
    assert sorted(df["region"]) == ["eu", "us"]
    assert sorted(df["amount"]) == [10, 20]
    assert "_id" in df.columns  # id preserved so a later update() round-trips


def test_read_streams_chunks_into_readresult(cluster) -> None:
    cluster.register_collection(
        location="acme",
        uuid=CID,
        slug="orders",
        rows=[{"n": 1}, {"n": 2}, {"n": 3}],
    )
    with _client(cluster) as cf:
        batches = list(cf.data.collection(CID).iter_batches())
    # one row per chunk from the fake -> three batches, all rows present
    assert sum(len(b) for b in batches) == 3
    assert len(batches) == 3


# -- slug resolution + cache through the real Client API -----------------


def test_slug_resolves_via_listing_and_reads(cluster) -> None:
    cluster.register_collection(
        location="acme", uuid=CID, slug="sales_orders", rows=[{"n": 1}, {"n": 2}]
    )
    with _client(cluster) as cf:
        col = cf.data.collection("sales_orders")
        assert len(col.read()) == 2
        assert col.collection_id == CID


def test_slug_resolution_cached_across_reads(cluster) -> None:
    cluster.register_collection(
        location="acme", uuid=CID, slug="sales_orders", rows=[{"n": 1}]
    )
    with _client(cluster) as cf:
        col = cf.data.collection("sales_orders")
        col.read()
        col.read()
        col.read()
    # one listing consulted for the slug, cached thereafter (per process)
    assert cluster.collections.get_all_calls == 1


def test_unknown_slug_raises_naming_slug_and_location(cluster) -> None:
    cluster.register_collection(location="acme", uuid=CID, slug="exists", rows=[])
    with _client(cluster) as cf, pytest.raises(NotFoundError, match="ghost") as exc:
        cf.data.collection("ghost").read()
    assert "acme" in str(exc.value)


def test_slug_cache_is_isolated_per_location(cluster) -> None:
    """A slug resolved for one tenant must not leak into another's cache."""
    cluster.register_collection(
        location="acme", uuid=CID, slug="orders", rows=[{"who": "acme"}]
    )
    cluster.register_collection(
        location="umbrella", uuid=CID2, slug="orders", rows=[{"who": "umbrella"}]
    )
    with _client(cluster) as cf:
        assert cf.data.collection("orders").collection_id == CID
        assert cf.with_location("umbrella").data.collection("orders").collection_id == CID2


def test_saved_query_reads_backing_collection(cluster) -> None:
    cluster.register_collection(
        location="acme", uuid=CID, slug="orders", rows=[{"revenue": 100}]
    )
    cluster.register_query(query_uuid=QID, collection_uuid=CID)
    with _client(cluster) as cf:
        df = cf.data.query(QID).read()
    assert list(df["revenue"]) == [100]


# -- retry behaviour on UNAVAILABLE --------------------------------------


def test_unavailable_is_retried_then_succeeds(cluster) -> None:
    """A read that UNAVAILABLEs once must transparently retry and then succeed.

    The fake fails the collection's first read and serves rows on the retry;
    with a 3-attempt policy the client's built-in retry config must absorb the
    failure so the caller never sees it.
    """
    cluster.register_collection(
        location="acme", uuid=CID, slug="warming", rows=[{"n": 1}], fail_unavailable=1
    )
    with _client(cluster, retries=RetryPolicy(max_attempts=3)) as cf:
        df = cf.data.collection(CID).read()
    assert list(df["n"]) == [1]
    assert cluster.aggregate.attempts[CID] == 2  # failed once, retried once


def test_unavailable_surfaces_as_transient_when_retries_exhausted(cluster) -> None:
    """When failures outlast the attempt budget, the typed TransientError shows."""
    cluster.register_collection(
        location="acme", uuid=CID, slug="down", rows=[{"n": 1}], fail_unavailable=5
    )
    with _client(cluster, retries=RetryPolicy(max_attempts=2)) as cf, pytest.raises(
        TransientError
    ):
        cf.data.collection(CID).read()


def test_no_retry_policy_does_not_retry_unavailable(cluster) -> None:
    """With retries disabled, the very first UNAVAILABLE surfaces immediately."""
    cluster.register_collection(
        location="acme", uuid=CID, slug="down", rows=[{"n": 1}], fail_unavailable=1
    )
    with _client(cluster, retries=None) as cf, pytest.raises(TransientError):
        cf.data.collection(CID).read()
    assert cluster.aggregate.attempts[CID] == 1  # no second attempt
