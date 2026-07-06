"""LocalMock transport double: stubs, call recording, and data round-trips.

Drives the mock through the real ``Clappform`` client and generated service
layer, which is how customers and the guide snippets in ``docs/snippets/``
use it.
"""

import pytest

from clappform import Clappform, ClappformError, _codec
from clappform.gen.clappform.data.v1.aggregate import aggregate_pb2
from clappform.gen.clappform.data.v1.insert import insert_pb2
from clappform.gen.clappform.data.v1.update import update_pb2
from clappform.testing import LocalMock, RecordedCall


@pytest.fixture
def cf():
    mock = LocalMock()
    client = Clappform("acme", "qa", api_key="test-key", transport=mock)
    yield client, mock
    client.close()


def test_stub_serves_canned_unary_response() -> None:
    mock = LocalMock()
    mock.on(
        "/clappform.data.v1.insert.InsertManagement/InsertSingle",
        insert_pb2.InsertResponse(processed_count=7, oids=["x"]),
    )
    cf = Clappform("acme", "qa", api_key="k", transport=mock)
    resp = cf.data.insert.insert_single(collection="orders", data=b"[]")
    assert resp.processed_count == 7
    assert list(resp.oids) == ["x"]


def test_stub_handler_receives_request(cf) -> None:
    client, mock = cf

    def handler(request):
        assert request.collection == "orders"
        return insert_pb2.InsertResponse(processed_count=1, oids=["from-handler"])

    mock.on("/clappform.data.v1.insert.InsertManagement/InsertSingle", handler)
    resp = client.data.insert.insert_single(collection="orders", data=b"[]")
    assert list(resp.oids) == ["from-handler"]


def test_calls_are_recorded_with_location(cf) -> None:
    client, mock = cf
    mock.on(
        "/clappform.data.v1.insert.InsertManagement/InsertSingle",
        insert_pb2.InsertResponse(processed_count=0),
    )
    client.data.insert.insert_single(collection="orders", data=b"[]")
    (call,) = mock.calls
    assert isinstance(call, RecordedCall)
    assert call.method.endswith("/InsertSingle")
    assert call.location == "acme"  # injected by the bound caller


def test_unknown_method_raises_helpful_error(cf) -> None:
    client, _mock = cf
    with pytest.raises(ClappformError, match="no response for"):
        client.data.change_request.request_change(collection="c", data=b"[]")


def test_seeded_read_streams_records(cf) -> None:
    client, mock = cf
    mock.seed("orders", [{"order_id": 1, "amount": 10.0}, {"order_id": 2, "amount": 20.0}])
    records = []
    for chunk in client.data.aggregate.aggregate_stream(collection="orders"):
        records.extend(_codec.bytes_to_records(chunk.data))
    assert [r["order_id"] for r in records] == [1, 2]
    assert all("_id" in r for r in records)  # synthetic ids assigned on seed


def test_seeded_read_respects_batch_size(cf) -> None:
    client, mock = cf
    mock.seed("orders", [{"i": i} for i in range(5)])
    sizes = [
        len(_codec.bytes_to_records(chunk.data))
        for chunk in client.data.aggregate.aggregate_stream(
            collection="orders", batch_size=2
        )
    ]
    assert sizes == [2, 2, 1]


def test_empty_collection_reads_one_empty_chunk(cf) -> None:
    client, mock = cf
    mock.seed("orders", [])
    chunks = list(client.data.aggregate.aggregate_stream(collection="orders"))
    assert len(chunks) == 1
    assert _codec.bytes_to_records(chunks[0].data) == []


def test_insert_single_appends_and_assigns_ids(cf) -> None:
    client, mock = cf
    resp = client.data.insert.insert_single(
        collection="orders", data=_codec.records_to_bytes([{"amount": 5}])
    )
    assert resp.processed_count == 1
    stored = mock.records("orders")
    assert len(stored) == 1
    assert stored[0]["amount"] == 5
    assert stored[0]["_id"] == list(resp.oids)[0]


def test_insert_many_stream_yields_response_per_request(cf) -> None:
    client, mock = cf
    requests = [
        insert_pb2.InsertRequest(
            collection="orders", data=_codec.records_to_bytes([{"n": 1}])
        ),
        insert_pb2.InsertRequest(
            collection="orders", data=_codec.records_to_bytes([{"n": 2}, {"n": 3}])
        ),
    ]
    responses = list(client.data.insert.insert_many(iter(requests)))
    assert [r.processed_count for r in responses] == [1, 2]
    assert len(mock.records("orders")) == 3


def test_read_mutate_update_round_trip(cf) -> None:
    client, mock = cf
    mock.seed("orders", [{"order_id": 1, "status": "open"}])
    # read
    (record,) = _codec.bytes_to_records(
        next(client.data.aggregate.aggregate_stream(collection="orders")).data
    )
    # mutate and update by _id (UpdateMany is stream-unary)
    record["status"] = "closed"
    client.data.update.update_many(
        [
            update_pb2.UpdateRequestByOid(
                collection="orders", data=_codec.records_to_bytes([record])
            )
        ]
    )
    assert mock.records("orders")[0]["status"] == "closed"


def test_delete_by_oids_removes_matching_rows(cf) -> None:
    client, mock = cf
    mock.seed("orders", [{"_id": "a"}, {"_id": "b"}, {"_id": "c"}])
    client.data.delete.delete_many_by_oids(collection="orders", oids=["a", "c"])
    assert [r["_id"] for r in mock.records("orders")] == ["b"]


def test_clear_empties_collection(cf) -> None:
    client, mock = cf
    mock.seed("orders", [{"_id": "a"}, {"_id": "b"}])
    client.data.delete.clear(collection="orders")
    assert mock.records("orders") == []


def test_explicit_stub_overrides_builtin_data_handler(cf) -> None:
    client, mock = cf
    mock.seed("orders", [{"_id": "a"}])
    mock.on(
        "/clappform.data.v1.aggregate.AggregateManagement/AggregateStream",
        [aggregate_pb2.AggregateResponse(data=b'[{"stubbed":true}]', total=1)],
    )
    (chunk,) = list(client.data.aggregate.aggregate_stream(collection="orders"))
    assert _codec.bytes_to_records(chunk.data) == [{"stubbed": True}]


def test_streaming_stub_must_be_iterable(cf) -> None:
    client, mock = cf
    mock.on(
        "/clappform.data.v1.aggregate.AggregateManagement/AggregateStream",
        aggregate_pb2.AggregateResponse(data=b"[]"),  # a bare message, not a list
    )
    with pytest.raises(ClappformError, match="must be an iterable"):
        list(client.data.aggregate.aggregate_stream(collection="orders"))


def test_reset_clears_state() -> None:
    mock = LocalMock()
    mock.seed("orders", [{"_id": "a"}]).on("/x/Y", object())
    mock.reset()
    assert mock.calls == []
    assert mock.records("orders") == []


def test_closed_mock_rejects_calls() -> None:
    mock = LocalMock()
    client = Clappform("acme", "qa", api_key="k", transport=mock)
    mock.close()  # a caller-owned transport is closed directly, not via client
    with pytest.raises(ClappformError, match="client is closed"):
        client.data.insert.insert_single(collection="orders", data=b"[]")
