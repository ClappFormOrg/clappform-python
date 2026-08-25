"""Runnable source for the quickstart snippets.

Every fenced block in docs/quickstart.md is pulled from this file by the
snippets extension, and this file runs end-to-end against ``LocalMock`` in the
docs-test job, so the quickstart cannot document code that no longer works.
The ``transport=LocalMock()`` argument is the only thing a reader drops to talk
to a real cluster; the seeding below stands in for data that already lives in
their tenant.
"""

from __future__ import annotations

from clappform.testing import LocalMock


def build_mock() -> LocalMock:
    """A mock seeded with the rows the quickstart reads back.

    ``cf.data.collection("sales_orders")`` resolves the slug to a UUID first, so
    the mock registers the slug->id mapping and seeds the store under that id.
    The actionflow ``start`` RPC is not a data-plane call, so it gets an
    explicit ``.on()`` stub keyed on its full gRPC method path.
    """
    from clappform.gen.clappform.client.v1.actionflow import actionflow_pb2

    mock = LocalMock()
    mock.seed_collection_slug("sales_orders", id="sales_orders-id")
    mock.seed(
        "sales_orders-id",
        [
            {"order_id": "A-1", "amount": 120.0, "status": "open", "region": "EU"},
            {"order_id": "A-2", "amount": 90.0, "status": "open", "region": "US"},
            {"order_id": "A-3", "amount": 40.0, "status": "closed", "region": "EU"},
        ],
    )
    mock.on(
        "/clappform.client.v1.actionflow.ActionflowManagement/Start",
        actionflow_pb2.StartActionflowResponse(message="started", uuid="run-abc123"),
    )
    return mock


def run(transport: LocalMock) -> None:
    # --8<-- [start:connect]
    from clappform import Clappform

    # location is your tenant subdomain (sent on every call); the cluster it
    # lives on is discovered from DNS, so this is all you normally need.
    cf = Clappform(
        location="acme",            # your tenant subdomain
        api_key="cf_live_...",      # the only credential v6 ships
    )

    # In air-gapped or split-DNS environments where discovery can't run, pin
    # the cluster explicitly, which skips DNS entirely.
    cf = Clappform(location="acme", cluster="prod", api_key="cf_live_...")
    # --8<-- [end:connect]

    # The env var is illustrative; set a placeholder so the block below runs in
    # CI without depending on the real environment. Not shown in the docs.
    import os

    os.environ.setdefault("CLAPPFORM_API_KEY", "cf_live_...")

    # --8<-- [start:connect-env]
    # Read the key from wherever your script keeps secrets; the library never
    # touches the environment itself, so this stays your choice.
    import os

    from clappform import Clappform

    cf = Clappform(location="acme", api_key=os.environ["CLAPPFORM_API_KEY"])
    # --8<-- [end:connect-env]

    # The docs example connects for real; the test swaps in a stubbed transport
    # so the round-trip below runs with no network.
    cf = Clappform(location="acme", cluster="prod", api_key="cf_live_...", transport=transport)

    with cf:
        # --8<-- [start:roundtrip]
        orders = cf.data.collection("sales_orders")

        # read a filtered slice straight into a pandas DataFrame by passing an
        # aggregation pipeline; $match filters, $project picks columns
        df = orders.read(
            pipeline=[
                {"$match": {"status": "open"}},
                {"$project": {"order_id": 1, "amount": 1, "region": 1}},
            ]
        )

        # mutate with plain pandas
        df["amount_eur"] = df["amount"] * 1.08

        # write the changed rows back, matched on _id (kept by read())
        orders.update(df)
        # --8<-- [end:roundtrip]

        assert len(df) == 2
        assert "amount_eur" in df.columns

        # --8<-- [start:full-task]
        # A complete task has the same shape almost every time: connect, read a
        # slice, transform it with plain pandas, write it back, and (optionally)
        # kick off a downstream flow. This is the whole loop end to end.
        orders = cf.data.collection("sales_orders")

        df = orders.read(pipeline=[{"$match": {"status": "open"}}])
        print(f"pulled {len(df)} open orders")   # pulled 2 open orders

        df["amount_eur"] = df["amount"] * 1.08
        df["priority"] = df["amount_eur"] > 100

        orders.update(df)                          # matched on _id, no args needed

        # trigger a downstream actionflow; the response carries the run's uuid
        started = cf.client.actionflow.start(id="recalculate-dashboards")
        print(f"started run {started.uuid}")       # started run run-abc123
        # --8<-- [end:full-task]
        assert started.uuid == "run-abc123"
        assert "priority" in df.columns


if __name__ == "__main__":
    run(build_mock())
