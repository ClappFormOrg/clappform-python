"""End-to-end transport behaviour against a real in-process gRPC server.

Covers the full stack: generated service layer -> bound caller -> transport
-> wire -> servicer, including metadata composition, deadlines, streaming,
and error translation. Only the data endpoint is overridden; nothing here
touches the network beyond 127.0.0.1.
"""

import threading
import time
from concurrent import futures

import grpc
import pytest

from clappform import (
    Clappform,
    ConfigurationError,
    NotFoundError,
    NotSupportedError,
    TransientError,
)
from clappform._transport import RetryPolicy
from clappform.gen.clappform.data.v1.aggregate import aggregate_pb2, aggregate_pb2_grpc
from clappform.gen.clappform.data.v1.insert import insert_pb2, insert_pb2_grpc


class InsertServicer(insert_pb2_grpc.InsertManagementServicer):
    def __init__(self) -> None:
        self.seen_metadata: dict[str, str] = {}

    def InsertSingle(self, request, context):
        self.seen_metadata = dict(context.invocation_metadata())
        if request.collection == "missing":
            context.abort(grpc.StatusCode.NOT_FOUND, "collection 'missing' not found")
        if request.collection == "no-tenant":
            context.abort(grpc.StatusCode.ABORTED, "invalid/missing header: 'location'")
        if request.collection == "slow":
            time.sleep(0.5)
        return insert_pb2.InsertResponse(processed_count=1, oids=["oid-1"])

    def InsertMany(self, request_iterator, context):
        for _request in request_iterator:
            yield insert_pb2.InsertResponse(processed_count=1)


# Set by the "endless" stream once the server sees the client cancel it.
ENDLESS_CANCELLED = threading.Event()


class AggregateServicer(aggregate_pb2_grpc.AggregateManagementServicer):
    def AggregateStream(self, request, context):
        if request.collection == "vanishes":
            # Yield one chunk, then fail mid-stream. Exercises the transport's
            # translating iterator, which must map the error raised *during*
            # iteration onto the typed hierarchy, not just errors at call time.
            yield aggregate_pb2.AggregateResponse(data=b"[1]", total=3)
            context.abort(grpc.StatusCode.NOT_FOUND, "collection vanished mid-scan")
        if request.collection == "endless":
            context.add_callback(ENDLESS_CANCELLED.set)
            for _ in range(500):
                if not context.is_active():
                    return
                yield aggregate_pb2.AggregateResponse(data=b"[1]")
                time.sleep(0.01)
            return
        for chunk in (b"[1]", b"[2]", b"[3]"):
            if request.collection == "slow-stream":
                time.sleep(0.15)
            yield aggregate_pb2.AggregateResponse(data=chunk, total=3)


@pytest.fixture(scope="module")
def server():
    insert_servicer = InsertServicer()
    grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    insert_pb2_grpc.add_InsertManagementServicer_to_server(insert_servicer, grpc_server)
    aggregate_pb2_grpc.add_AggregateManagementServicer_to_server(
        AggregateServicer(), grpc_server
    )
    port = grpc_server.add_insecure_port("127.0.0.1:0")
    grpc_server.start()
    yield f"127.0.0.1:{port}", insert_servicer
    grpc_server.stop(grace=None)


@pytest.fixture
def cf(server):
    address, _servicer = server
    client = Clappform(
        "acme",
        "qa",
        api_key="test-key",
        endpoints={"data": address},
        insecure=True,
        timeout=5.0,
        retries=RetryPolicy(max_attempts=2),
    )
    yield client
    client.close()


def test_unary_call_roundtrip_with_metadata(cf, server) -> None:
    _address, servicer = server
    response = cf.data.insert.insert_single(collection="orders", data=b"[]")
    assert response.processed_count == 1
    assert servicer.seen_metadata["x-api-key"] == "test-key"
    assert servicer.seen_metadata["location"] == "acme"


def test_per_call_location_overrides_metadata(cf, server) -> None:
    _address, servicer = server
    cf.data.insert.insert_single(collection="orders", location="umbrella")
    assert servicer.seen_metadata["location"] == "umbrella"


def test_server_streaming_iterates_chunks(cf) -> None:
    chunks = list(cf.data.aggregate.aggregate_stream(collection="orders"))
    assert [c.data for c in chunks] == [b"[1]", b"[2]", b"[3]"]
    assert chunks[0].total == 3


def test_streaming_error_mid_iteration_is_translated(cf) -> None:
    stream = cf.data.aggregate.aggregate_stream(collection="vanishes")
    first = next(stream)
    assert first.data == b"[1]"  # one chunk streamed before the failure
    with pytest.raises(NotFoundError, match="collection vanished mid-scan") as excinfo:
        next(stream)
    # context carried through even though the error surfaced mid-iteration
    assert "cluster='qa'" in str(excinfo.value)
    assert "location='acme'" in str(excinfo.value)


def test_not_found_translates(cf) -> None:
    with pytest.raises(NotFoundError, match="collection 'missing' not found") as excinfo:
        cf.data.insert.insert_single(collection="missing")
    assert "cluster='qa'" in str(excinfo.value)
    assert "location='acme'" in str(excinfo.value)


def test_discovered_cluster_flag_reaches_a_real_rpc_error(server, monkeypatch) -> None:
    # When the cluster was discovered (no explicit cluster=), a real RPC failure
    # carries the (discovered) marker end to end, so an operator seeing the
    # error can tell a wrong discovery from a wrong explicit cluster.
    from clappform import _discovery

    address, _servicer = server
    monkeypatch.setattr(_discovery, "discover_cluster", lambda location: "qa")
    client = Clappform(
        "acme",
        api_key="test-key",
        endpoints={"data": address},
        insecure=True,
        timeout=5.0,
        retries=RetryPolicy(max_attempts=2),
    )
    try:
        assert client.cluster_discovered is True
        with pytest.raises(NotFoundError) as excinfo:
            client.data.insert.insert_single(collection="missing")
        assert "cluster='qa' (discovered)" in str(excinfo.value)
    finally:
        client.close()


def test_missing_location_server_detail_becomes_configuration_error(cf) -> None:
    with pytest.raises(ConfigurationError, match="location="):
        cf.data.insert.insert_single(collection="no-tenant")


def test_unregistered_service_maps_to_not_supported(cf) -> None:
    with pytest.raises(NotSupportedError, match="may not serve this RPC yet"):
        cf.data.delete.clear(collection="orders")


def test_deadline_exceeded_translates_to_transient(cf) -> None:
    with pytest.raises(TransientError) as excinfo:
        cf.data.insert.insert_single(collection="slow", timeout=0.05)
    assert excinfo.value.status == "DEADLINE_EXCEEDED"


def test_unreachable_endpoint_translates_to_transient() -> None:
    cf = Clappform(
        "acme",
        "qa",
        api_key="k",
        endpoints={"data": "127.0.0.1:1"},
        insecure=True,
        timeout=1.0,
        retries=None,
    )
    try:
        with pytest.raises(TransientError):
            cf.data.insert.insert_single(collection="orders")
    finally:
        cf.close()


def test_retry_policy_service_config_shape() -> None:
    import json

    config = json.loads(RetryPolicy(max_attempts=3).service_config())
    policy = config["methodConfig"][0]["retryPolicy"]
    assert policy["maxAttempts"] == 3
    assert policy["retryableStatusCodes"] == ["UNAVAILABLE"]


# --- deadlines, cancellation and request-side failures -------------------------

def _short_deadline_client(server) -> Clappform:
    address, _servicer = server
    return Clappform(
        "acme", "qa", api_key="k", endpoints={"data": address}, insecure=True, timeout=0.2
    )


def test_streams_have_no_default_deadline(server) -> None:
    # 3 chunks at 0.15s each outlast the 0.2s unary deadline; a stream must not
    # inherit it, or every large read fails after `timeout` seconds.
    with _short_deadline_client(server) as cf:
        chunks = list(cf.data.aggregate.aggregate_stream(collection="slow-stream"))
        assert len(chunks) == 3
        with pytest.raises(TransientError):
            cf.data.insert.insert_single(collection="slow")


def test_per_call_timeout_still_bounds_a_stream(cf) -> None:
    with pytest.raises(TransientError):
        list(cf.data.aggregate.aggregate_stream(collection="slow-stream", timeout=0.2))


def test_stream_timeout_sets_a_client_wide_stream_deadline(server) -> None:
    address, _servicer = server
    with Clappform(
        "acme", "qa", api_key="k", endpoints={"data": address}, insecure=True,
        stream_timeout=0.2,
    ) as cf, pytest.raises(TransientError):
        list(cf.data.aggregate.aggregate_stream(collection="slow-stream"))


def test_abandoned_stream_is_cancelled_on_the_server(cf) -> None:
    ENDLESS_CANCELLED.clear()
    stream = cf.data.aggregate.aggregate_stream(collection="endless")
    next(stream)
    stream.close()
    assert ENDLESS_CANCELLED.wait(2), "server never saw the call end"


def test_request_producer_error_reaches_the_caller(cf) -> None:
    def requests():
        yield insert_pb2.InsertRequest(collection="c", data=b"[]")
        raise RuntimeError("boom in producer")

    with pytest.raises(RuntimeError, match="boom in producer"):
        list(cf.data.insert.insert_many(requests()))
