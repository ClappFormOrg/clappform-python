"""Runnable source for the migration guide snippets.

The guide shows old 5.x code beside its v6 replacement. The *old* blocks are
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
    from clappform.gen.clappform.data.v1.update import update_pb2
    from clappform.testing import _local_mock

    # include_unreleased=True emulates update() and delete(where=), which the
    # Data Connector does not serve yet; the guide marks both with a warning.
    mock = LocalMock(include_unreleased=True)
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
    mock.on(
        "/clappform.data.v1.update.UpdateManagement/ReplaceMany",
        update_pb2.UpdateRequest(),
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
    _stub_listing(mock)
    return mock


def _stub_listing(mock: LocalMock) -> None:
    from clappform.gen.clappform.client.v1.query import query_pb2
    from clappform.gen.clappform.v1.commons import commons_pb2

    mock.on(
        "/clappform.client.v1.query.QueryManagement/GetAll",
        query_pb2.Queries(
            queries=[query_pb2.Query(id="q-1", name="monthly-revenue")],
            pagination=commons_pb2.Pagination(page=1, pages=1, total=1),
        ),
    )


def run(transport: LocalMock) -> None:
    # --8<-- [start:connect]
    from clappform import Clappform

    # One client for every API. Pass your 5.x token as api_key=; it travels in
    # the same x-api-key header. The cluster is discovered from DNS, so there
    # is no target host:port to spell out.
    cf = Clappform(location="preprod", api_key="cf_live_...")

    # Or name the cluster your old target pointed at:
    #   data.clappform.com:50051 -> cluster=""    (the main cluster, still :50051)
    #   data-qa.clappform.com    -> cluster="qa"  (every other cluster: TLS on 443)
    cf = Clappform(location="preprod", cluster="qa", api_key="cf_live_...")
    # --8<-- [end:connect]

    cf = Clappform(
        location="preprod", cluster="", api_key="cf_live_...", transport=transport
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
        # New: append() chunks (2500 rows by default, as before) and streams
        # for you, and returns the rows the server acknowledged.
        new_rows = pd.DataFrame([{"order_id": "A-3", "amount": 55.0, "status": "open"}])
        written = cf.data.collection("sales_orders").append(new_rows)
        # --8<-- [end:insert]
        assert written == 1

        # --8<-- [start:replace-many]
        # The RPC 5.x's update_replace_many called is still there. It replaces
        # each document by _id; read() gives _id as the hex string it expects.
        orders = cf.data.collection("sales_orders")
        payload = df.to_json(orient="records", date_format="iso").encode("utf-8")
        cf.data.update.replace_many(collection=orders.collection_id, data=payload)
        # --8<-- [end:replace-many]

        # --8<-- [start:update]
        # New: read keeps _id, so mutate and hand the frame back. update() sets
        # only the frame's columns and leaves the rest of each document alone.
        df["amount"] = df["amount"] * 1.1
        cf.data.collection("sales_orders").update(df[["_id", "amount"]])
        # --8<-- [end:update]

        # --8<-- [start:upsert]
        # New in v6: insert-or-update keyed on a business column. A matched
        # document is replaced by its row, so send whole rows without _id.
        cf.data.collection("sales_orders").upsert(df.drop(columns="_id"), on="order_id")
        # --8<-- [end:upsert]
        assert len(transport.records("sales_orders-id")) == 3

        # --8<-- [start:delete]
        orders = cf.data.collection("sales_orders")

        # by explicit _id(s), the direct replacement for delete_many_by_oids
        orders.delete(oids=["order-id-1", "order-id-2"])

        # ...or by filter, evaluated server-side (not served yet, see below)
        orders.delete(where={"status": "cancelled"})
        # --8<-- [end:delete]

        # --8<-- [start:listing]
        # New in v6: every listing RPC gets a get_all() for one page and an
        # iter_get_all() that requests page after page until the last one.
        for query in cf.client.query.iter_get_all():
            print(query.id, query.name)

        first_page = cf.client.query.get_all(page=1, limit=50)  # limit = page size
        # --8<-- [end:listing]
        assert first_page.pagination.total == 1

        # --8<-- [start:actionflow]
        # Old: c.actionflow_start(actionflow_pb2.StartActionflow(id=..., custom_keys=...))
        # New: the same fields as keyword arguments, on the same client.
        started = cf.client.actionflow.start(id="recalculate-dashboards")
        # --8<-- [end:actionflow]
        assert started is not None

        # --8<-- [start:errors]
        # Old: except grpc.RpcError as e: if e.code() == grpc.StatusCode.NOT_FOUND: ...
        # New: catch the typed exception; no grpc import.
        from clappform import NotFoundError

        try:
            cf.data.collection("no-such-collection").read()
        except NotFoundError as exc:
            print(f"missing: {exc}")
        # --8<-- [end:errors]


if __name__ == "__main__":
    run(build_mock())
