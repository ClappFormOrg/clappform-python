"""Runnable source for the migration guide snippets.

The guide shows old 4.x/5.x code beside its v6 replacement. The *old* blocks are
illustrative only (that package isn't installed here), so they live in the
guide as plain fenced code. Every *v6* block is pulled from this file and runs
against ``LocalMock`` in the docs-test job, so the "after" side of every mapping
is guaranteed to work.
"""

from __future__ import annotations

import pandas as pd

from clappform.testing import LocalMock


def build_mock() -> LocalMock:
    import json

    from clappform.gen.clappform.client.v1.actionflow import actionflow_pb2
    from clappform.gen.clappform.data.v1.aggregate import aggregate_pb2
    from clappform.testing import _local_mock

    mock = LocalMock()
    mock.seed_collection_slug("sales_orders", id="sales_orders-id")
    mock.seed(
        "sales_orders-id",
        [
            {"order_id": "A-1", "amount": 120.0, "status": "open"},
            {"order_id": "A-2", "amount": 90.0, "status": "open"},
        ],
    )
    mock.on(
        "/clappform.client.v1.actionflow.ActionflowManagement/Start",
        actionflow_pb2.StartActionflowResponse(message="started", uuid="run-1"),
    )

    # The guide's aggregate() example uses a $group, which the seeded double
    # doesn't compute, so stub the server's grouped answer and delegate every
    # other read to the built-in handler.
    def _aggregate(request):
        stages = json.loads(request.pipeline) if request.pipeline else []
        if any("$group" in s for s in stages):
            grouped = [{"_id": "open", "total": 210.0}]
            return [aggregate_pb2.AggregateResponse(data=json.dumps(grouped).encode())]
        return _local_mock._handle_aggregate_stream(
            mock, "unary_stream", request, aggregate_pb2.AggregateResponse
        )

    mock.on(
        "/clappform.data.v1.aggregate.AggregateManagement/AggregateStream", _aggregate
    )
    return mock


def run(transport: LocalMock) -> None:
    # Old: clappform.Data(token, location) + clappform.Client(token, location)
    # New: one client for every API. The cluster is discovered from DNS, so you
    # no longer spell out a `target` host:port.
    # --8<-- [start:connect]
    from clappform import Clappform

    cf = Clappform(location="preprod", api_key="cf_live_...")
    # data-plane calls live on cf.data, client-API calls on cf.client:
    # one binding, no separate Data / Client objects.
    # --8<-- [end:connect]

    cf = Clappform(
        location="preprod", cluster="prod", api_key="cf_live_...", transport=transport
    )

    with cf:
        # --8<-- [start:read]
        # Old: build AggregateStreamRequest, json.dumps the pipeline, then
        #      pd.concat([pd.DataFrame(json.loads(x.data)) for x in d.aggregate(req)])
        # New: pass the pipeline straight to read(); you get a DataFrame back,
        # already decoded and concatenated. read() with no pipeline reads the
        # whole collection.
        df = cf.data.collection("sales_orders").read(
            pipeline=[{"$match": {"status": "open"}}]
        )
        # --8<-- [end:read]
        assert len(df) == 2

        # --8<-- [start:aggregate]
        # A full pipeline (the old default) still works; pass it to aggregate().
        # No json.dumps, no encode(), no manual concat of the streamed chunks.
        revenue = cf.data.collection("sales_orders").aggregate(
            [{"$group": {"_id": "$status", "total": {"$sum": "$amount"}}}]
        )
        # --8<-- [end:aggregate]
        assert "total" in revenue.columns

        # --8<-- [start:insert]
        # Old: clappform.utils.insert_many_dataframe(collection, df, size=...)
        #      then list(client.insert_many(request))
        # New: append() chunks and streams for you, and returns rows written.
        new_rows = pd.DataFrame([{"order_id": "A-3", "amount": 55.0, "status": "open"}])
        written = cf.data.collection("sales_orders").append(new_rows)
        # --8<-- [end:insert]
        assert written == 1

        # --8<-- [start:update]
        # Old: batch the frame yourself, to_json each batch, wrap in
        #      UpdateRequestByOid(data=...encode()), call update_replace_many.
        # New: read keeps _id, so mutate and hand the frame back.
        df["amount"] = df["amount"] * 1.1
        cf.data.collection("sales_orders").update(df)
        # --8<-- [end:update]

        # --8<-- [start:delete]
        orders = cf.data.collection("sales_orders")

        # by explicit _id(s), the direct replacement for delete_many_by_oids
        orders.delete(oids=["order-id-1", "order-id-2"])

        # ...or by filter, evaluated server-side (nothing round-trips)
        orders.delete(where={"status": "cancelled"})
        # --8<-- [end:delete]

        # --8<-- [start:actionflow]
        # Old: clappform.Client(...).actionflow_start(
        #          actionflow_pb2.StartActionflow(actionflowid=ID, user=4, ...))
        # New: on the same client, by id.
        started = cf.client.actionflow.start(id="recalculate-dashboards")
        # --8<-- [end:actionflow]
        assert started is not None


if __name__ == "__main__":
    run(build_mock())
