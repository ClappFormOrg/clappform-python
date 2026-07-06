"""Runnable source for the DataFrame-flows guide snippets.

Covers the read/filter, batch, append/update/upsert, replace-where and delete
paths. Runs against ``LocalMock`` in CI so the guide's code matches the client.
"""

from __future__ import annotations

from clappform.testing import LocalMock


def build_mock() -> LocalMock:
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
    from clappform import Clappform

    cf = Clappform(location="acme", cluster="prod", api_key="cf_live_...", transport=transport)

    with cf:
        # --8<-- [start:read]
        orders = cf.data.collection("sales_orders")

        # `where`, `fields` and `limit` are client-side sugar compiled into a
        # $match / $project / $limit pipeline — the API never sees the kwargs.
        df = orders.read(
            where={"status": "open"},
            fields=["order_id", "amount", "region"],
            limit=1000,
        )
        # --8<-- [end:read]
        assert len(df) == 2

        # --8<-- [start:aggregate]
        # For stages the sugar does not emit ($group, $sort, ...) pass a full
        # pipeline. It is sent through untouched.
        by_region = orders.aggregate(
            [
                {"$match": {"status": "open"}},
                {"$group": {"_id": "$region", "total": {"$sum": "$amount"}}},
            ]
        )
        # --8<-- [end:aggregate]
        # The pipeline reaches the collection intact; LocalMock executes the
        # $match it understands (2 open rows) and passes $group through without
        # evaluating it, so this asserts the call round-trips, not that the mock
        # reimplements $group.
        assert len(by_region) == 2

        # --8<-- [start:batches]
        # Memory-bounded reads: one list of records per gRPC chunk, nothing
        # fully materialised. Ask the server to cap each chunk with batch_size.
        for batch in orders.iter_batches(where={"status": "open"}, batch_size=500):
            handle(batch)
        # --8<-- [end:batches]

        # --8<-- [start:write]
        # read -> mutate -> write-back. update() keys on _id by default, which
        # read() keeps as a column, so the round-trip needs no `on=`.
        df["amount"] = df["amount"] * 1.08
        orders.update(df)

        # insert brand-new rows
        new_rows = df.head(0).assign(order_id=["A-9"], amount=[10.0], region=["EU"])
        orders.append(new_rows)

        # insert-or-update on a business key (no default — `on` is required)
        orders.upsert(df, on="order_id")
        # --8<-- [end:write]

        # --8<-- [start:server-side]
        # Mutate or delete without pulling rows through the client.
        orders.replace_where({"status": "open"}, {"reviewed": True})
        orders.delete(where={"status": "closed"})
        # --8<-- [end:server-side]

        # --8<-- [start:saved-query]
        # A saved server-side query carries its own collection + pipeline.
        revenue = cf.data.query("monthly-revenue-per-region")
        revenue_df = revenue.read()
        # --8<-- [end:saved-query]
        # The saved query reads the same backing collection this snippet has
        # been mutating, so it returns whatever rows now remain — assert it
        # tracks the live store rather than a hard-coded count.
        assert len(revenue_df) == len(transport.records("sales_orders-id"))
        assert len(revenue_df) > 0


def handle(batch: list) -> None:
    """Stand-in for whatever the caller does with each batch."""
    assert isinstance(batch, list)


if __name__ == "__main__":
    mock = build_mock()
    mock.seed_query("monthly-revenue-per-region", collection="sales_orders-id")
    run(mock)
