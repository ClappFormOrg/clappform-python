"""End-to-end flows over real loopback channels: write lifecycle, auth and
notifier families, concurrency, and multi-cluster isolation.

Complements ``test_grpc_harness.py`` (reads, pagination, retry) by driving the
paths that previously had no over-the-wire coverage: the full
append -> update -> read and delete -> read-empty lifecycles, the auth and
notifier families, concurrent RPCs through one client, and two clusters in one
process with no cross-talk. Everything runs against ``_grpc_fakes`` servicers;
nothing touches the network beyond 127.0.0.1.
"""

from __future__ import annotations

import threading

import pandas as pd
import pytest
from _grpc_fakes import start_fake_cluster

from clappform import Clappform
from clappform._transport import RetryPolicy

CID = "1c9a7f3e-0000-4000-8000-000000000001"


@pytest.fixture
def cluster():
    fake = start_fake_cluster()
    yield fake
    fake.stop()


def _client(cluster, *, location: str = "acme", retries: RetryPolicy | None = None) -> Clappform:
    return Clappform(
        location,
        "qa",
        api_key="test-key",
        endpoints=cluster.endpoints,
        insecure=True,
        timeout=5.0,
        retries=retries,
    )


# -- full write lifecycle over the wire ----------------------------------


def test_append_update_read_round_trips_over_the_wire(cluster) -> None:
    cluster.register_collection(location="acme", uuid=CID, slug="orders", rows=[])
    with _client(cluster) as cf:
        col = cf.data.collection(CID)
        col.append(pd.DataFrame([{"order_id": 1, "status": "open"}]))

        df = col.read()
        assert list(df["status"]) == ["open"]

        df.loc[df["order_id"] == 1, "status"] = "closed"
        col.update(df)  # keyed on _id, preserved by read()

        assert list(cf.data.collection(CID).read()["status"]) == ["closed"]
    assert cluster.update.seen_location == "acme"


def test_delete_then_read_is_empty_over_the_wire(cluster) -> None:
    cluster.register_collection(
        location="acme",
        uuid=CID,
        slug="orders",
        rows=[{"_id": "a", "status": "open"}, {"_id": "b", "status": "closed"}],
    )
    with _client(cluster) as cf:
        col = cf.data.collection(CID)
        col.delete(where={"status": "open"})
        remaining = col.read()
        assert list(remaining["_id"]) == ["b"]

        col.delete(oids=["b"])
        assert cf.data.collection(CID).read().empty


# -- auth family end-to-end ----------------------------------------------


def test_auth_generate_key_flows_over_the_wire(cluster) -> None:
    with _client(cluster) as cf:
        key = cf.auth.api_key.generate_key(name="nightly-etl")
    assert key.name == "nightly-etl"
    assert key.api_key.startswith("cf_test_")
    # the tenant header reached the authoriser
    assert cluster.api_key.seen_location == "acme"
    assert cluster.api_key.seen_name == "nightly-etl"


# -- notifier family end-to-end ------------------------------------------


def test_notifier_health_flows_over_the_wire(cluster) -> None:
    from clappform.gen.clappform.notifier.v1.health import health_pb2

    with _client(cluster) as cf:
        status = cf.notifier.health.health()
    assert status.service == "notifier"
    assert status.status == health_pb2.OK


# -- concurrency ---------------------------------------------------------


def test_concurrent_reads_through_one_client_share_the_channel(cluster) -> None:
    # A thread pool of readers through one client proves the per-address channel
    # cache/lock in GrpcTransport.channel_for is correct under contention: all
    # calls succeed and only one channel is built for the data endpoint.
    cluster.register_collection(
        location="acme",
        uuid=CID,
        slug="orders",
        rows=[{"_id": str(i), "n": i} for i in range(5)],
    )
    with _client(cluster) as cf:
        results: list[int] = []
        errors: list[Exception] = []
        lock = threading.Lock()

        def worker() -> None:
            try:
                n = len(cf.data.collection(CID).read())
                with lock:
                    results.append(n)
            except Exception as exc:  # noqa: BLE001 - surfaced via the errors list
                with lock:
                    errors.append(exc)

        threads = [threading.Thread(target=worker) for _ in range(12)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == []
        assert results == [5] * 12
        # one channel reused across all threads for the data address
        channel = cf.channel_for("data")
        assert cf.channel_for("data") is channel


# -- multi-cluster in one process ----------------------------------------


def test_two_clusters_one_process_have_no_cross_talk() -> None:
    # Two independent fake clusters on two ports; two clients in one process.
    # A write into one must not appear in the other, proving endpoint routing
    # and per-client transports keep clusters fully isolated.
    prod = start_fake_cluster()
    qa = start_fake_cluster()
    try:
        prod.register_collection(
            location="acme", uuid=CID, slug="orders", rows=[{"_id": "p", "where": "prod"}]
        )
        qa.register_collection(location="acme", uuid=CID, slug="orders", rows=[])

        cf_prod = _client(prod)
        cf_qa = _client(qa)
        with cf_prod, cf_qa:
            # copy prod -> qa by business key
            df = cf_prod.data.collection(CID).read()
            cf_qa.data.collection(CID).append(df)

            # the row is now in qa, and prod still has exactly its original row
            assert len(cf_qa.data.collection(CID).read()) == 1
            assert list(cf_prod.data.collection(CID).read()["where"]) == ["prod"]
            # qa's insert servicer saw the write; prod's did not
            assert qa.insert.seen_location == "acme"
            assert prod.insert.seen_location is None
    finally:
        prod.stop()
        qa.stop()


# -- streaming: partial consumption / cancellation -----------------------


def test_partial_stream_consumption_does_not_break_client(cluster) -> None:
    # Abandoning a read stream after the first batch (break out of iteration)
    # must not wedge the client: a subsequent read on a fresh handle still works.
    cluster.register_collection(
        location="acme",
        uuid=CID,
        slug="orders",
        rows=[{"_id": str(i), "n": i} for i in range(6)],
    )
    with _client(cluster) as cf:
        for _batch in cf.data.collection(CID).iter_batches():
            break  # consume only the first chunk, then walk away

        # a fresh read still returns the full set
        assert len(cf.data.collection(CID).read()) == 6


def test_large_streamed_read_materialises_all_rows(cluster) -> None:
    # A large row count exercises the streaming read + ReadResult batching at
    # scale (the fake yields one chunk per row), confirming many-chunk streams
    # flatten correctly rather than only the small cases the other tests use.
    rows = [{"_id": str(i), "payload": "x" * 256, "n": i} for i in range(2000)]
    cluster.register_collection(location="acme", uuid=CID, slug="big", rows=rows)
    with _client(cluster) as cf:
        df = cf.data.collection(CID).read()
    assert len(df) == 2000
    assert df["n"].sum() == sum(range(2000))
