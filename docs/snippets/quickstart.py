"""Runnable source for the quickstart snippets.

Every fenced block in docs/quickstart.md is pulled from this file by the
snippets extension, and this file runs end-to-end against ``LocalMock`` in the
docs-test job — so the quickstart cannot document code that no longer works.
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
    """
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
    return mock


def run(transport: LocalMock) -> None:
    # --8<-- [start:connect]
    from clappform import Clappform

    cf = Clappform(
        location="acme",            # your tenant subdomain, sent on every call
        cluster="prod",             # host extension; omit to discover it via DNS
        api_key="cf_live_...",      # the only credential v6 ships
    )
    # --8<-- [end:connect]

    # The docs example connects for real; the test swaps in a stubbed transport
    # so the round-trip below runs with no network.
    cf = Clappform(location="acme", cluster="prod", api_key="cf_live_...", transport=transport)

    with cf:
        # --8<-- [start:roundtrip]
        orders = cf.data.collection("sales_orders")

        # read a filtered slice straight into a pandas DataFrame
        df = orders.read(where={"status": "open"}, fields=["order_id", "amount", "region"])

        # mutate with plain pandas
        df["amount_eur"] = df["amount"] * 1.08

        # write the changed rows back, matched on _id (kept by read())
        orders.update(df)
        # --8<-- [end:roundtrip]

        assert len(df) == 2
        assert "amount_eur" in df.columns


if __name__ == "__main__":
    run(build_mock())
