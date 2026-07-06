"""Runnable source for the error-handling & retries guide snippets."""

from __future__ import annotations

from clappform.testing import LocalMock


def build_mock() -> LocalMock:
    # One real collection is registered, so slug resolution runs — but "ghost"
    # is not in the listing, so resolving it raises NotFoundError, the real path
    # the snippet catches below.
    mock = LocalMock()
    mock.seed_collection_slug("real-collection", id="real-collection-id")
    mock.seed("real-collection-id", [{"_id": "1", "value": 1}])
    return mock


def run(transport: LocalMock) -> None:
    # --8<-- [start:retry-policy]
    from clappform import DEFAULT_RETRIES, Clappform, RetryPolicy

    # Retries are configured once on the client and applied by gRPC's built-in
    # retry support. DEFAULT_RETRIES retries UNAVAILABLE with backoff; override
    # per client when you need a different policy (or None to disable).
    patient = RetryPolicy(max_attempts=6, initial_backoff="0.5s", max_backoff="10s")
    cf = Clappform(location="acme", cluster="prod", api_key="cf_live_...", retries=patient)
    _ = (DEFAULT_RETRIES, cf)
    # --8<-- [end:retry-policy]

    cf = Clappform(location="acme", cluster="prod", api_key="cf_live_...", transport=transport)

    with cf:
        # --8<-- [start:typed-errors]
        from clappform import NotFoundError, TransientError

        orders = cf.data.collection("ghost")  # no such slug in this tenant
        try:
            orders.read()
        except NotFoundError as exc:
            # Every error carries call context — method, cluster, location — so
            # "which tenant on which cluster failed" is in the message.
            handle_missing(exc)
        except TransientError:
            # Retries were configured and still exhausted; safe to retry the
            # whole flow or surface a degraded state to the caller.
            retry_later()
        # --8<-- [end:typed-errors]


def handle_missing(exc: Exception) -> None:
    assert "location" in str(exc)


def retry_later() -> None:  # pragma: no cover - not reached with the seeded mock
    pass


if __name__ == "__main__":
    run(build_mock())
