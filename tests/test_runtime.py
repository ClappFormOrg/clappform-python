"""Behaviour of the transport seam helpers in clappform._runtime."""

import pytest

from clappform import _runtime
from clappform.gen.clappform.data.v1.insert import insert_pb2


def test_build_request_from_kwargs() -> None:
    request = _runtime.build_request(
        insert_pb2.InsertRequest, None, {"collection": "orders", "data": b"[]"}
    )
    assert request.collection == "orders"
    assert request.data == b"[]"


def test_build_request_passthrough() -> None:
    original = insert_pb2.InsertRequest(collection="orders")
    assert _runtime.build_request(insert_pb2.InsertRequest, original, {}) is original


def test_build_request_rejects_message_plus_kwargs() -> None:
    original = insert_pb2.InsertRequest(collection="orders")
    with pytest.raises(TypeError, match="not both"):
        _runtime.build_request(insert_pb2.InsertRequest, original, {"data": b"x"})


def test_build_request_rejects_wrong_message_type() -> None:
    with pytest.raises(TypeError, match="InsertRequest"):
        _runtime.build_request(insert_pb2.InsertRequest, object(), {})


def test_ensure_iterable_validates_lazily() -> None:
    items = [insert_pb2.InsertRequest(collection="a"), "not-a-message"]
    iterator = _runtime.ensure_iterable(items, insert_pb2.InsertRequest)
    assert next(iterator).collection == "a"
    with pytest.raises(TypeError, match="stream items"):
        next(iterator)
