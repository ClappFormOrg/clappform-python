"""Runnable source for the DataFrame-flows guide snippets.

Covers the read/filter, batch, aggregate (collection pipeline + saved query),
append/update/upsert/sync, replace-where and delete paths. Runs against
``LocalMock`` in CI so the guide's code matches the client.
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
        # pipeline to aggregate(). It is sent to the server untouched and the
        # result comes back as a DataFrame — one row per group here.
        revenue_by_region = orders.aggregate(
            [
                {"$match": {"status": "open"}},
                {"$group": {"_id": "$region", "total": {"$sum": "$amount"}}},
                {"$sort": {"total": -1}},
            ]
        )
        # --8<-- [end:aggregate]
        # The pipeline reaches the collection intact; LocalMock executes the
        # $match it understands (2 open rows) and passes $group/$sort through
        # without evaluating them, so this asserts the call round-trips, not
        # that the mock reimplements an aggregation engine.
        assert len(revenue_by_region) == 2

        # --8<-- [start:aggregate-query]
        # A saved server-side query already carries its own collection and
        # pipeline, so you just read it — no pipeline to write client-side.
        revenue = cf.data.query("monthly-revenue-per-region")
        revenue_df = revenue.read()
        # --8<-- [end:aggregate-query]
        # The saved query reads the same backing collection, so it tracks the
        # live store rather than a hard-coded count.
        assert len(revenue_df) == len(transport.records("sales_orders-id"))

        # --8<-- [start:batches]
        # Memory-bounded reads: one list of records per gRPC chunk, nothing
        # fully materialised. Ask the server to cap each chunk with batch_size.
        for batch in orders.iter_batches(where={"status": "open"}, batch_size=500):
            handle(batch)
        # --8<-- [end:batches]

        # --8<-- [start:insert]
        # append() inserts every row as a brand-new document. Build the frame
        # however you like — here from a list of dicts.
        import pandas as pd

        new_orders = pd.DataFrame(
            [
                {"order_id": "A-9", "amount": 10.0, "status": "open", "region": "EU"},
                {"order_id": "A-10", "amount": 25.0, "status": "open", "region": "US"},
            ]
        )
        written = orders.append(new_orders)  # returns the row count written
        # --8<-- [end:insert]
        assert written == 2

        # --8<-- [start:update]
        # read -> mutate -> write-back. update() keys on _id by default, which
        # read() keeps as a column, so the round-trip needs no `on=`. Only the
        # rows you changed are sent.
        open_orders = orders.read(where={"status": "open"})
        open_orders["amount"] = open_orders["amount"] * 1.08  # 8% uplift
        orders.update(open_orders)
        # --8<-- [end:update]

        # --8<-- [start:upsert]
        # upsert() inserts-or-updates on a business key — no _id needed. `on`
        # has no default: you must name the key column. Rows whose key exists
        # are updated in place; the rest are inserted.
        incoming = pd.DataFrame(
            [
                {"order_id": "A-1", "amount": 200.0, "status": "open", "region": "EU"},
                {"order_id": "A-99", "amount": 5.0, "status": "open", "region": "APAC"},
            ]
        )
        orders.upsert(incoming, on="order_id")
        # --8<-- [end:upsert]
        # A-1 updated in place, A-99 inserted — no duplicate A-1.
        by_key = {row["order_id"]: row for row in transport.records("sales_orders-id")}
        assert by_key["A-1"]["amount"] == 200.0
        assert by_key["A-99"]["region"] == "APAC"

        # --8<-- [start:server-side]
        # Mutate or delete without pulling rows through the client. Both run
        # entirely on the server — nothing is round-tripped.
        orders.replace_where({"status": "open"}, {"reviewed": True})
        orders.delete(where={"status": "closed"})

        # Delete specific rows by their _id instead of a filter.
        stale = orders.read(where={"region": "APAC"})
        orders.delete(oids=list(stale["_id"]))
        # --8<-- [end:server-side]
        assert not any(row.get("region") == "APAC" for row in transport.records("sales_orders-id"))

        # --8<-- [start:clear]
        # clear() empties the whole collection. It is separate from delete() by
        # design, so a full wipe is never an accident of an empty filter.
        orders.clear()
        # --8<-- [end:clear]
        assert transport.records("sales_orders-id") == []


def handle(batch: list) -> None:
    """Stand-in for whatever the caller does with each batch."""
    assert isinstance(batch, list)


if __name__ == "__main__":
    mock = build_mock()
    mock.seed_query("monthly-revenue-per-region", collection="sales_orders-id")
    run(mock)
