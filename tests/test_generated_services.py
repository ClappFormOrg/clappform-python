"""Behaviour of the committed generated service layer, driven by a fake caller.

These tests exercise the real shipped modules under clappform.services:
kwargs flattening, streaming adapters, and pagination, against an in-memory
Caller, so they cover exactly what users import.
"""

from collections.abc import Iterator

import pytest

from clappform.gen.clappform.client.v1.query import query_pb2
from clappform.gen.clappform.data.v1.insert import insert_pb2
from clappform.gen.clappform.v1.commons import commons_pb2
from clappform.services.client import ClientAPI
from clappform.services.data import DataAPI


class RecordingCaller:
    """Caller double: records invocations, returns queued responses."""

    def __init__(self) -> None:
        self.calls: list[dict] = []
        self.responses: list = []

    def invoke(self, kind, method, request, request_cls, response_cls, **options):
        if kind in ("stream_unary", "stream_stream"):
            request = list(request)  # drain the adapter so validation runs
        self.calls.append(
            {
                "kind": kind,
                "method": method,
                "request": request,
                "options": options,
            }
        )
        if self.responses:
            return self.responses.pop(0)
        if kind.endswith("_stream"):
            return iter(())
        return response_cls()


def test_unary_call_builds_request_from_kwargs() -> None:
    caller = RecordingCaller()
    data = DataAPI(caller)

    response = data.insert.insert_single(data=b"[]", collection="orders", location="acme")

    assert isinstance(response, insert_pb2.InsertResponse)
    call = caller.calls[0]
    assert call["kind"] == "unary_unary"
    assert call["method"] == "/clappform.data.v1.insert.InsertManagement/InsertSingle"
    assert call["request"].collection == "orders"
    assert call["options"]["location"] == "acme"
    assert call["options"]["timeout"] is None


def test_unary_call_accepts_prebuilt_message() -> None:
    caller = RecordingCaller()
    data = DataAPI(caller)
    request = insert_pb2.InsertRequest(collection="orders")

    data.insert.insert_single(request)

    assert caller.calls[0]["request"] is request


def test_unary_call_rejects_message_plus_kwargs() -> None:
    data = DataAPI(RecordingCaller())
    with pytest.raises(TypeError, match="not both"):
        data.insert.insert_single(insert_pb2.InsertRequest(), collection="orders")


def test_stream_input_adapter_validates_items() -> None:
    caller = RecordingCaller()
    data = DataAPI(caller)
    requests = [insert_pb2.InsertRequest(collection="orders", data=b"[]")]

    data.insert.insert_patched(requests)

    call = caller.calls[0]
    assert call["kind"] == "stream_unary"
    assert call["request"][0].collection == "orders"

    with pytest.raises(TypeError, match="stream items"):
        data.insert.insert_patched(["nope"])


def test_bidi_streaming_returns_iterator() -> None:
    caller = RecordingCaller()
    caller.responses.append(iter([insert_pb2.InsertResponse(processed_count=7)]))
    data = DataAPI(caller)

    result = data.insert.insert_many([insert_pb2.InsertRequest(collection="orders")])

    assert isinstance(result, Iterator)
    assert next(result).processed_count == 7
    assert caller.calls[0]["kind"] == "stream_stream"


def test_iter_pagination_walks_all_pages() -> None:
    caller = RecordingCaller()
    caller.responses = [
        query_pb2.Queries(
            queries=[query_pb2.Query(id="q1"), query_pb2.Query(id="q2")],
            pagination=commons_pb2.Pagination(page=1, pages=2),
        ),
        query_pb2.Queries(
            queries=[query_pb2.Query(id="q3")],
            pagination=commons_pb2.Pagination(page=2, pages=2),
        ),
    ]
    client = ClientAPI(caller)

    ids = [q.id for q in client.query.iter_get_all(limit=2, location="acme")]

    assert ids == ["q1", "q2", "q3"]
    assert [c["request"].page for c in caller.calls] == [1, 2]
    assert all(c["request"].limit == 2 for c in caller.calls)
    assert all(c["options"]["location"] == "acme" for c in caller.calls)


def test_iter_pagination_stops_when_pagination_unset() -> None:
    caller = RecordingCaller()
    caller.responses = [query_pb2.Queries(queries=[query_pb2.Query(id="only")])]
    client = ClientAPI(caller)

    assert [q.id for q in client.query.iter_get_all()] == ["only"]
    assert len(caller.calls) == 1
