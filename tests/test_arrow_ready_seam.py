"""Phase-0 Arrow-readiness invariants of the read seam.

The read path is required to be *format-aware from day one*: the codec consumes
a stream of ``(format, bytes)`` chunks and dispatches per chunk, and
``ReadResult`` holds discrete batches lazily (one gRPC response = one batch)
rather than eagerly concatenating into a single blob. These properties are what
let an ``ARROW_IPC`` branch land later as a new case, not a rewrite. This module
pins those invariants so a refactor can't quietly regress the seam back into a
JSON-hardcoded read path.
"""

from __future__ import annotations

import pytest

from clappform import _codec
from clappform._codec import ChunkFormat
from clappform.dataframes import ReadResult


def test_codec_dispatches_per_chunk_format_not_globally() -> None:
    # A stream whose chunks carry different formats must be dispatched per
    # chunk: the JSON chunk decodes, and the ARROW_IPC chunk hits the reserved
    # branch and raises, proving the format travels with each chunk rather than
    # being assumed once for the whole stream.
    stream = [
        (ChunkFormat.JSON, b'[{"a":1}]'),
        (ChunkFormat.ARROW_IPC, b"\x00arrow"),
    ]
    it = _codec.records_from_chunks(stream)
    assert next(it) == {"a": 1}  # first (JSON) chunk decodes
    with pytest.raises(NotImplementedError, match="arrow_ipc"):
        next(it)  # second chunk dispatches to the reserved Arrow branch


def test_chunkformat_reserves_arrow_without_wiring_it() -> None:
    # The enum reserves the Arrow case (Phase 1 wires it); it must exist so the
    # request/response format can be represented, but decoding it is not yet
    # implemented.
    assert ChunkFormat.ARROW_IPC.value == "arrow_ipc"
    assert ChunkFormat.JSON.value == "json"
    with pytest.raises(NotImplementedError):
        _codec.bytes_to_records(b"anything", ChunkFormat.ARROW_IPC)


def test_readresult_consumes_batches_lazily_one_at_a_time() -> None:
    # ReadResult must not eagerly pull/concatenate all chunks: iterating it
    # should draw from the underlying chunk stream on demand, one batch at a
    # time. A generator that records how far it has been advanced proves the
    # laziness (a batch is only produced after its chunk is pulled).
    pulled: list[int] = []

    def chunks():
        for i in range(3):
            pulled.append(i)
            yield ChunkFormat.JSON, _codec.records_to_bytes([{"n": i}])

    result = ReadResult(chunks())
    batches = result.iter_batches()

    # Nothing pulled until the first batch is requested.
    assert pulled == []
    first = next(batches)
    assert first == [{"n": 0}]
    assert pulled == [0]  # exactly one chunk drawn, not all three
    second = next(batches)
    assert second == [{"n": 1}]
    assert pulled == [0, 1]


def test_readresult_keeps_batches_discrete_not_concatenated() -> None:
    # One gRPC response = one batch: iter_batches yields a separate list per
    # chunk (not a single flattened blob), which is the seam a streaming Arrow
    # reader plugs into (one Arrow record batch per chunk).
    chunks = [
        (ChunkFormat.JSON, _codec.records_to_bytes([{"n": 0}, {"n": 1}])),
        (ChunkFormat.JSON, _codec.records_to_bytes([{"n": 2}])),
    ]
    result = ReadResult(iter(chunks))
    batches = list(result.iter_batches())
    assert batches == [[{"n": 0}, {"n": 1}], [{"n": 2}]]  # boundaries preserved


def test_readresult_flat_iteration_still_flattens_across_batches() -> None:
    # Row-wise iteration flattens across the discrete batches, so callers that
    # want records don't see the chunk boundaries.
    chunks = [
        (ChunkFormat.JSON, _codec.records_to_bytes([{"n": 0}])),
        (ChunkFormat.JSON, _codec.records_to_bytes([{"n": 1}, {"n": 2}])),
    ]
    result = ReadResult(iter(chunks))
    assert list(result) == [{"n": 0}, {"n": 1}, {"n": 2}]
