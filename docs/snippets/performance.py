"""Runnable source for the performance & large-datasets guide snippets.

Covers batch_size on reads, chunk_rows + progress on writes, and streaming vs
materialising. Runs against LocalMock in CI.
"""

from __future__ import annotations

import pandas as pd

from clappform.testing import LocalMock


def build_mock() -> LocalMock:
    mock = LocalMock()
    mock.seed_collection_slug("events", id="events-id")
    mock.seed("events-id", [{"n": i} for i in range(1, 31)])
    mock.seed_collection_slug("target", id="target-id")
    mock.seed("target-id", [])
    return mock


def run(transport: LocalMock) -> None:
    from clappform import Clappform

    cf = Clappform(location="acme", cluster="prod", api_key="cf_live_...", transport=transport)

    with cf:
        events = cf.data.collection("events")
        target = cf.data.collection("target")

        # --8<-- [start:read-batch-size]
        # batch_size caps rows per gRPC chunk on a read. Larger = fewer
        # round-trips (faster, more memory); smaller = leaner peak memory. Tune
        # to your row width, not a fixed number.
        for batch in events.fetch(batch_size=5_000).iter_batches():
            handle(batch)
        # --8<-- [end:read-batch-size]

        # --8<-- [start:write-progress]
        # append/update/upsert stream the upload in chunks of chunk_rows. Pass a
        # progress callback to surface a running count: a notebook progress bar,
        # a log line, whatever. It's called with the cumulative rows after each
        # chunk.
        big = pd.DataFrame([{"n": i} for i in range(10_000)])

        def on_progress(rows_written: int) -> None:
            print(f"  ... {rows_written} rows written")

        written = target.append(big, chunk_rows=5_000, progress=on_progress)
        # --8<-- [end:write-progress]
        assert written == 10_000

        # --8<-- [start:stream-not-materialise]
        # For a reduce-and-discard job, stream batches instead of read()/to_pandas
        # so peak memory is one chunk. This holds one batch at a time.
        total = 0
        for batch in events.iter_batches(batch_size=10_000):
            total += len(batch)
        # --8<-- [end:stream-not-materialise]
        assert total == 30


def handle(batch: list) -> None:
    assert isinstance(batch, list)


if __name__ == "__main__":
    run(build_mock())
