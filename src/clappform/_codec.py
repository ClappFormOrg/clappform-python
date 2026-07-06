"""Data-plane JSON codec: records <-> bytes, with type normalisation.

This is the encoding used by every DataFrame flow. It is deliberately
pandas-independent — it speaks *records* (lists of plain dicts) in and out, so
pandas is only ever applied at the very edge (``DataFrame(records)`` /
``df.to_dict("records")``) and alternative surfaces (polars, Arrow) can be
added without reworking the flows here.

The wire carries result-set data in opaque ``bytes`` fields
(``InsertRequest.data``, ``AggregateResponse.data``, update/delete payloads).
Today those bytes are JSON; a columnar Arrow format is planned as an additive
branch. To keep that additive, the read side is structured around a
``(format, bytes)`` pair rather than assuming "bytes are always JSON": callers
above this module pass the format the server reported, and only the
``ChunkFormat.JSON`` branch is wired up here.

Encoding rules (mirroring what the gateway's JSON handling expects):

* ``NaN`` / ``NaT`` / ``None`` -> JSON ``null``.
* ``datetime`` / ``date`` -> ISO-8601 strings.
* Mongo Extended JSON v2 forms in *incoming* data (``{"$oid": ...}``,
  ``{"$date": ...}``) are parsed to plain Python types so a round-trip does
  not leave wrapper dicts in user DataFrames.
* ``_id`` is kept as an ordinary column on the way in, so a read -> mutate ->
  update round-trip can key on it without special handling.

Uploads are chunked at ``DEFAULT_CHUNK_ROWS`` rows, matching 5.x behaviour, so
a failed chunk is retryable at the flow level rather than re-sending the whole
frame.
"""

from __future__ import annotations

import json
import math
from collections.abc import Iterable, Iterator, Mapping
from datetime import date, datetime, timezone
from enum import Enum
from typing import Any

Record = dict[str, Any]

DEFAULT_CHUNK_ROWS = 2500


class ChunkFormat(str, Enum):
    """Wire format of a data chunk's ``bytes`` payload.

    Only ``JSON`` is decoded today. ``ARROW_IPC`` is reserved so the read path
    can branch on the server-reported format once an Arrow output surface
    ships, without changing this module's shape.
    """

    JSON = "json"
    ARROW_IPC = "arrow_ipc"


def _normalise_value(value: Any) -> Any:
    """Convert one Python value to its JSON-serialisable form.

    ``NaN``/``NaT`` collapse to ``None``; datetimes become ISO-8601 strings;
    containers are normalised recursively so nested frames encode correctly.
    """
    if value is None:
        return None
    if isinstance(value, float):
        # Covers both plain float NaN and pandas NaT/NA, which compare unequal
        # to themselves. isnan rejects non-floats, so guard on float first.
        if math.isnan(value):
            return None
        return value
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, Mapping):
        return {str(k): _normalise_value(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_normalise_value(v) for v in value]
    # Missing-value singletons (pandas NaT/NA, numpy NaT) that slipped past the
    # float branch compare unequal to themselves. pandas NA is doubly awkward:
    # ``NA != NA`` returns NA, not a bool, and coercing that to bool raises
    # "boolean value of NA is ambiguous" — so route any non-bool / raising
    # comparison to None too, since only these missing sentinels behave that way.
    if _is_missing_sentinel(value):
        return None
    return value


def _is_missing_sentinel(value: Any) -> bool:
    """True for a value that is unequal to itself (NaN/NaT/NA-style missing).

    Written to survive comparison operators that do not return a plain bool
    (pandas ``NA`` returns ``NA`` from ``!=`` and raises on truth-testing):
    such values are themselves missing sentinels, so treat them as missing.
    """
    try:
        return bool(value != value)  # noqa: PLR0124 -- NaN/NaT/NA sentinel check
    except (TypeError, ValueError):
        return True


def _parse_extended_json(value: Any) -> Any:
    """Collapse Mongo Extended JSON v2 wrappers to plain Python values.

    ``{"$oid": "..."}`` becomes the hex string; ``{"$date": ...}`` becomes an
    ISO-8601 string (the value is already ISO-8601 or epoch-ms per the v2
    spec — epoch-ms is converted, strings pass through). Anything that is not a
    recognised wrapper is returned structurally unchanged.
    """
    if isinstance(value, list):
        return [_parse_extended_json(v) for v in value]
    if not isinstance(value, dict):
        return value
    if len(value) == 1:
        key, inner = next(iter(value.items()))
        if key == "$oid" and isinstance(inner, str):
            return inner
        if key == "$date":
            if isinstance(inner, dict) and "$numberLong" in inner:
                inner = inner["$numberLong"]
            if isinstance(inner, (int, str)) and not isinstance(inner, bool):
                try:
                    millis = int(inner)
                except (TypeError, ValueError):
                    return inner
                return datetime.fromtimestamp(millis / 1000, tz=timezone.utc).isoformat()
            return inner
    return {k: _parse_extended_json(v) for k, v in value.items()}


def records_to_bytes(records: Iterable[Record]) -> bytes:
    """Encode a batch of records as a single JSON array of objects."""
    normalised = [_normalise_value(dict(record)) for record in records]
    return json.dumps(normalised, separators=(",", ":")).encode("utf-8")


def chunk_records(
    records: Iterable[Record],
    chunk_rows: int = DEFAULT_CHUNK_ROWS,
) -> Iterator[bytes]:
    """Yield JSON-encoded chunks of at most ``chunk_rows`` records each.

    Empty input yields nothing (no empty chunk is sent). A non-positive
    ``chunk_rows`` is a caller error.
    """
    if chunk_rows <= 0:
        raise ValueError(f"chunk_rows must be positive, got {chunk_rows}")
    batch: list[Record] = []
    for record in records:
        batch.append(record)
        if len(batch) >= chunk_rows:
            yield records_to_bytes(batch)
            batch = []
    if batch:
        yield records_to_bytes(batch)


def bytes_to_records(data: bytes, fmt: ChunkFormat = ChunkFormat.JSON) -> list[Record]:
    """Decode one chunk's ``bytes`` payload into records.

    Extended JSON v2 wrappers are collapsed to plain values. An empty payload
    (server sends ``b""`` for an empty result) decodes to no records.
    """
    if fmt is not ChunkFormat.JSON:
        raise NotImplementedError(
            f"decoding {fmt.value!r} chunks is not supported yet; "
            "only JSON result data is handled by this client version"
        )
    if not data:
        return []
    decoded = json.loads(data)
    if isinstance(decoded, dict):
        decoded = [decoded]
    if not isinstance(decoded, list):
        raise ValueError(
            f"expected a JSON array or object in result data, got {type(decoded).__name__}"
        )
    records: list[Record] = []
    for item in decoded:
        parsed = _parse_extended_json(item)
        if not isinstance(parsed, dict):
            raise ValueError(
                f"expected result rows to be objects, got {type(parsed).__name__}"
            )
        records.append(parsed)
    return records


def records_from_chunks(
    chunks: Iterable[tuple[ChunkFormat, bytes]],
) -> Iterator[Record]:
    """Flatten a stream of ``(format, bytes)`` chunks into records.

    This is the read-side seam the Arrow path plugs into: an ``ARROW_IPC``
    branch becomes a new case here, not a rewrite of every caller.
    """
    for fmt, data in chunks:
        yield from bytes_to_records(data, fmt)


def encode_pipeline(pipeline: Any) -> bytes:
    """Encode an aggregation pipeline as JSON bytes for the wire.

    The pipeline goes across as JSON regardless of the collection's storage
    backend: the server reads the bytes into a map and, for Mongo-backed
    collections, converts that map to BSON itself; Elastic-backed collections
    consume the JSON (Elastic DSL) directly. Values are normalised the same
    way record data is (``NaN``/``NaT`` -> ``null``, datetimes -> ISO-8601), so
    a pipeline referencing timestamps encodes consistently with the rows.
    """
    return json.dumps(_normalise_value(pipeline), separators=(",", ":")).encode("utf-8")


# Retained alias: the pipeline encoding was originally named for the Elastic
# path before it was confirmed to be the single JSON encoding for all backends.
encode_elastic_pipeline = encode_pipeline
