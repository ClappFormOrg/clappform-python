"""Data-plane JSON codec: encoding rules, round-trips, and error handling."""

import json
import math
from datetime import date, datetime, timezone

import pytest

from clappform import _codec
from clappform._codec import ChunkFormat


def test_records_to_bytes_is_compact_json_array() -> None:
    data = _codec.records_to_bytes([{"a": 1}, {"a": 2}])
    assert data == b'[{"a":1},{"a":2}]'
    assert json.loads(data) == [{"a": 1}, {"a": 2}]


def test_nan_and_none_become_null() -> None:
    data = _codec.records_to_bytes([{"x": float("nan"), "y": None, "z": 1.5}])
    assert json.loads(data) == [{"x": None, "y": None, "z": 1.5}]


def test_datetime_and_date_become_iso8601() -> None:
    row = {"ts": datetime(2020, 1, 2, 3, 4, 5), "d": date(2021, 6, 7)}
    assert json.loads(_codec.records_to_bytes([row])) == [
        {"ts": "2020-01-02T03:04:05", "d": "2021-06-07"}
    ]


def test_nested_containers_are_normalised() -> None:
    row = {"items": [{"v": float("nan")}, {"v": 2}], "meta": {"at": date(2020, 1, 1)}}
    assert json.loads(_codec.records_to_bytes([row])) == [
        {"items": [{"v": None}, {"v": 2}], "meta": {"at": "2020-01-01"}}
    ]


def test_id_is_preserved_across_round_trip() -> None:
    records = [{"_id": "abc", "amount": 10}]
    decoded = _codec.bytes_to_records(_codec.records_to_bytes(records))
    assert decoded == [{"_id": "abc", "amount": 10}]


def test_bytes_to_records_accepts_single_object() -> None:
    assert _codec.bytes_to_records(b'{"a":1}') == [{"a": 1}]


def test_empty_payload_decodes_to_no_records() -> None:
    assert _codec.bytes_to_records(b"") == []


def test_extended_json_oid_and_date_are_collapsed() -> None:
    payload = b'[{"_id":{"$oid":"deadbeef"},"created":{"$date":"2021-05-06T00:00:00Z"}}]'
    assert _codec.bytes_to_records(payload) == [
        {"_id": "deadbeef", "created": "2021-05-06T00:00:00Z"}
    ]


def test_extended_json_date_epoch_millis_is_converted() -> None:
    millis = int(datetime(2021, 1, 1, tzinfo=timezone.utc).timestamp() * 1000)
    payload = json.dumps([{"d": {"$date": {"$numberLong": str(millis)}}}]).encode()
    (record,) = _codec.bytes_to_records(payload)
    assert record["d"].startswith("2021-01-01T00:00:00")


def test_chunk_records_splits_on_row_count() -> None:
    chunks = list(_codec.chunk_records(({"i": i} for i in range(5)), chunk_rows=2))
    assert [len(_codec.bytes_to_records(c)) for c in chunks] == [2, 2, 1]


def test_chunk_records_empty_input_yields_nothing() -> None:
    assert list(_codec.chunk_records([])) == []


def test_chunk_records_rejects_non_positive_size() -> None:
    with pytest.raises(ValueError, match="chunk_rows must be positive"):
        list(_codec.chunk_records([{"a": 1}], chunk_rows=0))


def test_records_from_chunks_flattens_format_pairs() -> None:
    chunks = [
        (ChunkFormat.JSON, b'[{"a":1}]'),
        (ChunkFormat.JSON, b'[{"a":2},{"a":3}]'),
    ]
    assert list(_codec.records_from_chunks(chunks)) == [{"a": 1}, {"a": 2}, {"a": 3}]


def test_arrow_format_is_not_yet_decodable() -> None:
    with pytest.raises(NotImplementedError, match="arrow_ipc"):
        _codec.bytes_to_records(b"...", ChunkFormat.ARROW_IPC)


def test_non_array_non_object_payload_is_rejected() -> None:
    with pytest.raises(ValueError, match="expected a JSON array or object"):
        _codec.bytes_to_records(b"42")


def test_array_of_scalars_is_rejected() -> None:
    with pytest.raises(ValueError, match="expected result rows to be objects"):
        _codec.bytes_to_records(b"[1,2,3]")


def test_encode_elastic_pipeline_normalises_and_serialises() -> None:
    encoded = _codec.encode_elastic_pipeline([{"match": {"ts": date(2020, 1, 1)}}])
    assert json.loads(encoded) == [{"match": {"ts": "2020-01-01"}}]


def test_float_nan_helper_is_json_null_not_string() -> None:
    # Regression guard: NaN must not leak through as the literal "NaN" that
    # json.dumps would otherwise emit for an unguarded float.
    data = _codec.records_to_bytes([{"x": math.nan}])
    assert b"NaN" not in data
