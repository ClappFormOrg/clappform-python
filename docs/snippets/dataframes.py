"""Runnable source for the DataFrame-flows guide snippets.

Covers the read/filter, batch, aggregate (collection pipeline + saved query),
append/update/upsert, update-where and delete paths, and the type mapping.
Runs against ``LocalMock`` in CI so the guide's code matches the client.
"""

from __future__ import annotations

from clappform.testing import LocalMock


def build_mock() -> LocalMock:
    # include_unreleased=True emulates update(), update_where() and
    # delete(where=), which the Data Connector does not serve yet; the guide
    # marks each of those blocks with a warning.
    mock = LocalMock(include_unreleased=True)
    mock.seed_collection_slug("sales_orders", id="sales_orders-id")
    mock.seed(
        "sales_orders-id",
        [
            {"order_id": "A-1", "amount": 120.0, "status": "open", "region": "EU"},
            {"order_id": "A-2", "amount": 90.0, "status": "open", "region": "US"},
            {"order_id": "A-3", "amount": 40.0, "status": "closed", "region": "EU"},
        ],
    )
    mock.seed_collection_slug("events", id="events-id")
    mock.seed("events-id", [])
    return mock


def _grouped_orders():
    """A handle whose reads return a server-computed ``$group`` result.

    LocalMock does not emulate ``$group`` and raises for it, so the aggregate
    block reads from a stubbed AggregateStream instead of the seeded store.
    """
    from clappform import Clappform
    from clappform.gen.clappform.data.v1.aggregate import aggregate_pb2

    stub = LocalMock().on(
        "/clappform.data.v1.aggregate.AggregateManagement/AggregateStream",
        [
            aggregate_pb2.AggregateResponse(
                data=b'[{"_id":"EU","total":120.0},{"_id":"US","total":90.0}]'
            )
        ],
    )
    cf = Clappform(location="acme", api_key="cf_live_...", transport=stub)
    return cf.data.collection("4a4f9a52-0000-4000-8000-000000000001")


def run(transport: LocalMock) -> None:
    from clappform import Clappform

    cf = Clappform(location="acme", cluster="", api_key="cf_live_...", transport=transport)

    with cf:
        # --8<-- [start:read]
        orders = cf.data.collection("sales_orders")

        # read() with no arguments streams the whole collection. To filter,
        # project or cap, pass an aggregation pipeline in the syntax the
        # collection's backend expects (Mongo stages here).
        df = orders.read(
            pipeline=[
                {"$match": {"status": "open"}},
                {"$project": {"order_id": 1, "amount": 1, "region": 1}},
                {"$limit": 1000},
            ]
        )
        # --8<-- [end:read]
        assert len(df) == 2

        seeded_orders = orders
        orders = _grouped_orders()
        # --8<-- [start:aggregate]
        # aggregate() is the DataFrame-returning twin of read(pipeline=...).
        # Reach for it for grouping/reshaping stages ($group, $sort, ...); the
        # server computes them and returns one row per group here.
        revenue_by_region = orders.aggregate(
            [
                {"$match": {"status": "open"}},
                {"$group": {"_id": "$region", "total": {"$sum": "$amount"}}},
                {"$sort": {"total": -1}},
            ]
        )
        # --8<-- [end:aggregate]
        assert list(revenue_by_region["_id"]) == ["EU", "US"]
        orders = seeded_orders

        # --8<-- [start:aggregate-query]
        # A saved server-side query already carries its own collection and
        # pipeline, so you read it by name with no pipeline to write.
        revenue = cf.data.query("monthly-revenue-per-region")
        revenue_df = revenue.read()
        # --8<-- [end:aggregate-query]
        # The saved query reads the same backing collection, so it tracks the
        # live store rather than a hard-coded count.
        assert len(revenue_df) == len(transport.records("sales_orders-id"))

        # --8<-- [start:batches]
        # Memory-bounded reads: one list of records per gRPC chunk, nothing
        # fully materialised. Ask the server to cap each chunk with batch_size.
        for batch in orders.iter_batches(
            pipeline=[{"$match": {"status": "open"}}], batch_size=500
        ):
            handle(batch)
        # --8<-- [end:batches]

        # --8<-- [start:insert]
        # append() inserts every row as a new document and returns the number
        # of rows the server acknowledged. The frame must not carry _id.
        import pandas as pd

        new_orders = pd.DataFrame(
            [
                {"order_id": "A-9", "amount": 10.0, "status": "open", "region": "EU"},
                {"order_id": "A-10", "amount": 25.0, "status": "open", "region": "US"},
            ]
        )
        written = orders.append(new_orders)
        # --8<-- [end:insert]
        assert written == 2

        # --8<-- [start:update]
        # read -> mutate -> write back. update() matches on _id by default,
        # which read() keeps as a column, and sets only the frame's columns.
        open_orders = orders.read(pipeline=[{"$match": {"status": "open"}}])
        open_orders["amount"] = open_orders["amount"] * 1.08  # 8% uplift
        orders.update(open_orders[["_id", "amount"]])

        # Match on another column with on=; every row needs a value for it.
        orders.update(open_orders[["order_id", "status"]], on="order_id")
        # --8<-- [end:update]
        by_key = {row["order_id"]: row for row in transport.records("sales_orders-id")}
        assert by_key["A-1"]["amount"] == 120.0 * 1.08
        assert by_key["A-1"]["region"] == "EU"  # fields not in the frame are left alone

        # --8<-- [start:upsert]
        # upsert() inserts-or-updates on a business key. `on` has no default.
        # A row whose key exists replaces that document; the rest are inserted.
        incoming = pd.DataFrame(
            [
                {"order_id": "A-1", "amount": 200.0, "status": "open", "region": "EU"},
                {"order_id": "A-99", "amount": 5.0, "status": "open", "region": "APAC"},
            ]
        )
        orders.upsert(incoming, on="order_id")
        # --8<-- [end:upsert]
        # A-1 updated in place, A-99 inserted, no duplicate A-1.
        by_key = {row["order_id"]: row for row in transport.records("sales_orders-id")}
        assert by_key["A-1"]["amount"] == 200.0
        assert by_key["A-99"]["region"] == "APAC"

        # --8<-- [start:server-side]
        # Set fields or delete by filter without pulling rows through the
        # client. Both run on the server.
        orders.update_where({"status": "open"}, {"reviewed": True})
        orders.delete(where={"status": "closed"})
        # --8<-- [end:server-side]
        stored = transport.records("sales_orders-id")
        assert not any(row.get("status") == "closed" for row in stored)

        # --8<-- [start:delete-oids]
        # Delete specific rows by their _id. This RPC is served today.
        stale = orders.read(pipeline=[{"$match": {"region": "APAC"}}])
        orders.delete(oids=list(stale["_id"]))
        # --8<-- [end:delete-oids]
        assert not any(row.get("region") == "APAC" for row in transport.records("sales_orders-id"))

        # --8<-- [start:types]
        # Values are converted to JSON on the way out. datetimes become
        # ISO-8601 strings and come back as strings, so parse them yourself.
        from datetime import datetime, timezone
        from decimal import Decimal

        events = cf.data.collection("events")
        events.append(
            pd.DataFrame(
                [
                    {
                        "kind": "signup",
                        "at": datetime(2026, 3, 1, 9, 30, tzinfo=timezone.utc),
                        "fee": Decimal("9.95"),
                        "score": float("nan"),
                    }
                ]
            )
        )
        df = events.read()
        df["at"] = pd.to_datetime(df["at"])  # the column arrives as str
        # --8<-- [end:types]
        assert str(df["at"].dtype).startswith("datetime64")
        assert df.loc[0, "fee"] == 9.95
        assert transport.records("events-id")[0]["score"] is None

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
