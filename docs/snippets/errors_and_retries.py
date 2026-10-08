"""Runnable source for the error-handling & retries guide snippets."""

from __future__ import annotations

from clappform.testing import LocalMock


def build_mock() -> LocalMock:
    # Two collections are registered, so slug resolution runs, but "ghost" is
    # not in the listing, so resolving it raises NotFoundError, the real path
    # the snippet catches below.
    mock = LocalMock()
    mock.seed_collection_slug("stock", id="stock-id")
    mock.seed("stock-id", [{"sku": "S-1", "qty": 4}, {"sku": "S-2", "qty": 0}])
    mock.seed_collection_slug("stock_mirror", id="stock_mirror-id")
    mock.seed("stock_mirror-id", [])
    mock.seed_collection_slug("events", id="events-id")
    mock.seed("events-id", [])
    return mock


def _fail_inserts(mock: LocalMock) -> None:
    """Make InsertMany fail the way a dropped connection does."""
    from clappform import TransientError

    def _unavailable(_requests):
        raise TransientError("connection reset", status="UNAVAILABLE")

    mock.on("/clappform.data.v1.insert.InsertManagement/InsertMany", _unavailable)


def run(transport: LocalMock) -> None:
    import pandas as pd

    # --8<-- [start:retry-policy]
    from clappform import DEFAULT_RETRIES, Clappform, RetryPolicy

    # Retries are configured once on the client and applied by gRPC's built-in
    # retry support. DEFAULT_RETRIES retries UNAVAILABLE with backoff; override
    # it per client (or pass retries=None to disable). Backoffs are seconds,
    # and max_attempts must be 2 to 5, the range gRPC honours.
    patient = RetryPolicy(max_attempts=5, initial_backoff=0.5, max_backoff=10.0)
    cf = Clappform(location="acme", api_key="cf_live_...", retries=patient)
    # --8<-- [end:retry-policy]
    assert DEFAULT_RETRIES.max_attempts == 4
    cf.close()

    # --8<-- [start:deadlines]
    # timeout= bounds each unary call (one request, one response); it defaults
    # to 60 seconds. stream_timeout= bounds each streaming call, which covers
    # every DataFrame read and write; it defaults to None, so a stream runs as
    # long as it keeps moving and keepalive detects a dead connection.
    cf = Clappform(location="acme", api_key="cf_live_...", timeout=30.0, stream_timeout=900.0)
    # --8<-- [end:deadlines]
    cf.close()

    cf = Clappform(location="acme", cluster="", api_key="cf_live_...", transport=transport)

    with cf:
        # --8<-- [start:typed-errors]
        from clappform import NotFoundError, TransientError

        orders = cf.data.collection("ghost")  # no such slug in this location
        try:
            orders.read()
        except NotFoundError as exc:
            # A ClappformError carries call context (method, cluster, location), so
            # "which tenant on which cluster failed" is in the message.
            handle_missing(exc)
        except TransientError:
            # UNAVAILABLE after the client's retries, or DEADLINE_EXCEEDED.
            retry_later()
        # --8<-- [end:typed-errors]

        _fail_inserts(transport)
        new_events = pd.DataFrame([{"event_id": "E-1", "kind": "signup"}])
        # --8<-- [start:append-failure]
        events = cf.data.collection("events")
        try:
            events.append(new_events)
        except TransientError as exc:
            # append() is never retried and is not idempotent: the rows the
            # server acknowledged stay inserted, and a chunk in flight may have
            # landed too. Finish the load with an upsert, which converges.
            print(f"append stopped after {exc.rows_written} acknowledged rows")
            events.upsert(new_events, on="event_id")
        # --8<-- [end:append-failure]
        assert [row["event_id"] for row in transport.records("events-id")] == ["E-1"]

        stock = cf.data.collection("stock")
        mirror = cf.data.collection("stock_mirror")

        # --8<-- [start:retry-flow]
        # The client retries reads on UNAVAILABLE, but never writes. A flow
        # built from reads and upserts is safe to run again, so retry it whole.
        import time

        for attempt in range(3):
            try:
                df = stock.read()
                mirror.upsert(df.drop(columns="_id"), on="sku")
                break
            except TransientError:
                if attempt == 2:
                    raise
                time.sleep(2**attempt)  # back off, then re-run the whole flow
        # --8<-- [end:retry-flow]
        assert len(transport.records("stock_mirror-id")) == 2

        # --8<-- [start:per-call-timeout]
        # timeout= on one call bounds that call, including the whole stream of
        # a read, without changing the client-wide defaults.
        df = stock.read(timeout=120.0)
        # --8<-- [end:per-call-timeout]
        assert transport.calls[-1].timeout == 120.0
        assert df is not None


def handle_missing(exc: Exception) -> None:
    assert "location" in str(exc)


def retry_later() -> None:  # pragma: no cover - not reached with the seeded mock
    pass


if __name__ == "__main__":
    run(build_mock())
