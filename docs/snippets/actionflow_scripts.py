"""Runnable source for the "running inside an actionflow" guide snippets.

Covers the in-worker context: constructing a client from values the worker
supplies, and passing start parameters to a flow. Only the shipped v6 API is
used here. Runs against ``LocalMock`` in the docs-test job.
"""

from __future__ import annotations

import json

from clappform.testing import LocalMock


def build_mock() -> LocalMock:
    from clappform.gen.clappform.client.v1.actionflow import actionflow_pb2

    mock = LocalMock()
    mock.seed_collection_slug("sales_orders", id="sales_orders-id")
    mock.seed("sales_orders-id", [{"order_id": "A-1", "amount": 10.0, "status": "open"}])
    mock.on(
        "/clappform.client.v1.actionflow.ActionflowManagement/Start",
        actionflow_pb2.StartActionflowResponse(message="started", uuid="run-xyz"),
    )
    return mock


def run(transport: LocalMock) -> None:
    from clappform import Clappform

    # In a real worker these come from the task's environment/parameters. We set
    # them as plain locals here so the snippet is self-contained.
    TENANT = "acme"
    API_KEY = "cf_live_..."

    # --8<-- [start:connect-in-worker]
    # A task running in the worker is handed its tenant and a key. Nothing is
    # read from the environment by the library — you pass them in, so pull them
    # from wherever the worker exposes them and construct the client explicitly.
    cf = Clappform(location=TENANT, api_key=API_KEY)
    # --8<-- [end:connect-in-worker]

    cf = Clappform(location=TENANT, cluster="prod", api_key=API_KEY, transport=transport)

    with cf:
        # --8<-- [start:start-params]
        # Start parameters ride on `custom_keys`, which today takes JSON bytes.
        # Build them from a plain dict — encode once, pass through.
        custom_keys = json.dumps({"next_page": "", "since": "2026-01-01"}).encode("utf-8")
        started = cf.client.actionflow.start(
            id="recalculate-dashboards",
            custom_keys=custom_keys,
        )
        run_id = started.uuid
        # --8<-- [end:start-params]
        assert run_id == "run-xyz"

        # --8<-- [start:read-write]
        # From there it's the ordinary DataFrame loop — nothing about running in
        # a worker changes how you read and write collections.
        orders = cf.data.collection("sales_orders")
        df = orders.read(pipeline=[{"$match": {"status": "open"}}])
        df["amount"] = df["amount"] * 1.1
        orders.update(df)
        # --8<-- [end:read-write]
        assert len(df) == 1


if __name__ == "__main__":
    run(build_mock())
