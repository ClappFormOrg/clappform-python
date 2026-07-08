"""Runnable source for the cookbook guide snippets.

Copy-paste recipes for the operations users reach for most: collection CRUD,
single-record reads, file ingest, aggregation, actionflow starts, index
management, and app transfer. Every block is pulled into docs/guides/cookbook.md
and runs against ``LocalMock`` in the docs-test job, so the recipes stay
correct.

Data-plane calls (read/append/update/delete/aggregate) run against the seeded
store. Everything else — actionflow start, index management, transfer — is not a
data-plane RPC, so it is backed by an explicit ``.on()`` stub keyed on the full
gRPC method path, exactly as you'd stub it in your own tests.
"""

from __future__ import annotations

import io
import json

import pandas as pd

from clappform.testing import LocalMock


def build_mock() -> LocalMock:
    from clappform.gen.clappform.client.v1.actionflow import actionflow_pb2
    from clappform.gen.clappform.client.v1.transfer import transfer_pb2
    from clappform.gen.clappform.data.v1.aggregate import aggregate_pb2
    from clappform.gen.clappform.data.v1.index import index_pb2
    from clappform.gen.clappform.v1.commons import commons_pb2
    from clappform.testing import _local_mock

    mock = LocalMock()
    mock.seed_collection_slug("housing_stock", id="housing_stock-id")
    mock.seed(
        "housing_stock-id",
        [
            {"address": "Herengracht 1", "city": "Amsterdam", "energy_label": "C"},
            {"address": "Keizersgracht 42", "city": "Amsterdam", "energy_label": "F"},
        ],
    )
    for slug in ("import_target", "change_requests", "empty_coll", "customers"):
        mock.seed_collection_slug(slug, id=f"{slug}-id")
        mock.seed(f"{slug}-id", [])
    # one seeded customer for the single-record read recipe
    mock.seed("customers-id", [{"email": "a@example.com", "plan": "pro", "seats": 3}])

    # $group isn't computed by the seeded double; stub the server's grouped
    # answer for that pipeline and delegate every other read to the built-in.
    def _aggregate(request):
        stages = json.loads(request.pipeline) if request.pipeline else []
        if any("$group" in s for s in stages):
            grouped = [{"_id": "C", "count": 1}, {"_id": "F", "count": 1}]
            return [aggregate_pb2.AggregateResponse(data=json.dumps(grouped).encode())]
        return _local_mock._handle_aggregate_stream(
            mock, "unary_stream", request, aggregate_pb2.AggregateResponse
        )

    mock.on("/clappform.data.v1.aggregate.AggregateManagement/AggregateStream", _aggregate)

    # Non-data-plane RPCs the recipes call.
    mock.on(
        "/clappform.client.v1.actionflow.ActionflowManagement/Start",
        actionflow_pb2.StartActionflowResponse(message="started", uuid="run-xyz"),
    )
    mock.on(
        "/clappform.data.v1.index.IndexManagement/Create",
        index_pb2.CreateIndexResponse(success=True),
    )
    mock.on(
        "/clappform.data.v1.index.IndexManagement/GetAll",
        index_pb2.ListIndexesResponse(
            indexes=[index_pb2.IndexInfo(name="_id_"), index_pb2.IndexInfo(name="city_1")]
        ),
    )
    mock.on(
        "/clappform.data.v1.index.IndexManagement/Delete",
        index_pb2.DeleteIndexResponse(success=True),
    )
    mock.on(
        "/clappform.client.v1.transfer.TransferManagement/ExportApp",
        transfer_pb2.AppExport(app=b'{"slug":"sales"}', queries=b"[]", actionflows=b"[]"),
    )
    mock.on(
        "/clappform.client.v1.transfer.TransferManagement/ImportApp",
        commons_pb2.Message(message="imported"),
    )
    return mock


def build_second_cluster_mock() -> LocalMock:
    mock = LocalMock()
    mock.seed_collection_slug("housing_stock", id="housing_stock-id")
    mock.seed("housing_stock-id", [])
    # the transfer recipe imports into this second client
    from clappform.gen.clappform.v1.commons import commons_pb2

    mock.on(
        "/clappform.client.v1.transfer.TransferManagement/ImportApp",
        commons_pb2.Message(message="imported"),
    )
    return mock


def run(transport: LocalMock, other_cluster: LocalMock) -> None:
    from clappform import Clappform

    cf = Clappform(
        location="acme", cluster="prod", api_key="cf_live_...", transport=transport
    )

    with cf:
        # ---- Collection CRUD ------------------------------------------------
        # --8<-- [start:crud-create]
        # CREATE — append new documents from a DataFrame. Returns rows written.
        rows = pd.DataFrame(
            [
                {"address": "Prinsengracht 3", "city": "Amsterdam", "energy_label": "B"},
                {"address": "Damrak 70", "city": "Amsterdam", "energy_label": "A"},
            ]
        )
        cf.data.collection("housing_stock").append(rows)
        # --8<-- [end:crud-create]

        # --8<-- [start:crud-read]
        # READ — a filtered slice straight into pandas. `where` filters,
        # `fields` projects, `limit` caps; all optional.
        df = cf.data.collection("housing_stock").read(
            pipeline=[
                {"$match": {"city": "Amsterdam"}},
                {"$project": {"address": 1, "energy_label": 1}},
                {"$limit": 1000},
            ]
        )
        # --8<-- [end:crud-read]
        assert len(df) >= 2

        # --8<-- [start:crud-update]
        # UPDATE — mutate the frame (which still carries _id) and hand it back.
        # Matched on _id by default, so no key argument is needed.
        df = cf.data.collection("housing_stock").read(
            pipeline=[{"$match": {"city": "Amsterdam"}}]
        )
        df["needs_audit"] = df["energy_label"].isin(["F", "G"])
        cf.data.collection("housing_stock").update(df)
        # --8<-- [end:crud-update]

        # --8<-- [start:crud-upsert]
        # UPSERT — insert-or-update keyed on a business column. Re-running never
        # duplicates: rows whose key exists are updated, the rest inserted.
        cf.data.collection("housing_stock").upsert(rows, on="address")
        # --8<-- [end:crud-upsert]

        # --8<-- [start:crud-delete]
        # DELETE — by explicit _id(s) or by a server-side filter.
        housing = cf.data.collection("housing_stock")
        housing.delete(where={"energy_label": "G"})     # by filter
        housing.delete(oids=["some-id-1", "some-id-2"])  # by id
        # To wipe the whole collection, call clear() — never delete(where={}).
        # --8<-- [end:crud-delete]

        # ---- Single-record read --------------------------------------------
        # --8<-- [start:single-read]
        # Fetch one document: $match filters, $limit caps at one row, then take
        # it as a dict.
        df = cf.data.collection("customers").read(
            pipeline=[{"$match": {"email": "a@example.com"}}, {"$limit": 1}]
        )
        customer = df.iloc[0].to_dict() if not df.empty else None
        # --8<-- [end:single-read]
        assert customer is not None and customer["plan"] == "pro"

        # ---- File ingest ----------------------------------------------------
        # --8<-- [start:ingest-file]
        # Load an uploaded file (bytes) into a DataFrame, then append it. Swap
        # read_csv for the reader matching the source:
        #   .xlsx    -> pd.read_excel(io.BytesIO(file_bytes))   # needs openpyxl
        #   .parquet -> pd.read_parquet(io.BytesIO(file_bytes))
        #   .json    -> pd.read_json(io.BytesIO(file_bytes))
        loaded = pd.read_csv(io.BytesIO(file_bytes))
        written = cf.data.collection("import_target").append(loaded)
        # --8<-- [end:ingest-file]
        assert written == 2

        # ---- Aggregate to a DataFrame --------------------------------------
        # --8<-- [start:aggregate-to-df]
        # Group server-side and get a DataFrame back — one result row per group.
        by_label = cf.data.collection("housing_stock").aggregate(
            [{"$group": {"_id": "$energy_label", "count": {"$sum": 1}}}]
        )
        # --8<-- [end:aggregate-to-df]
        assert "count" in by_label.columns

        # ---- Empty result --------------------------------------------------
        # --8<-- [start:empty-read]
        # A read matching nothing returns an empty frame (no columns), never an
        # error — so branch on .empty before indexing a column.
        df = cf.data.collection("empty_coll").read(
            pipeline=[{"$match": {"status": "open"}}]
        )
        if df.empty:
            print("nothing to process")
        else:
            df["processed"] = True
            cf.data.collection("empty_coll").update(df)
        # --8<-- [end:empty-read]
        assert df.empty

        # ---- Change request ------------------------------------------------
        # --8<-- [start:change-request]
        # A change request is a row in its collection: build a dict, wrap it in
        # a one-row frame, append.
        record = {
            "cf_original_id": "obj-123",
            "status": "requested",
            "changes": [{"key": "energy_label", "old": "F", "new": "C"}],
        }
        cf.data.collection("change_requests").append(pd.DataFrame([record]))
        # --8<-- [end:change-request]

        # ---- Actionflow start ----------------------------------------------
        # --8<-- [start:actionflow-start]
        # Trigger a flow by id; the response carries the run's uuid.
        started = cf.client.actionflow.start(id="recalculate-dashboards")
        run_id = started.uuid
        # --8<-- [end:actionflow-start]
        assert run_id == "run-xyz"

        # --8<-- [start:actionflow-params]
        # With start parameters — custom_keys takes JSON bytes today, so encode
        # a plain dict.
        cf.client.actionflow.start(
            id="recalculate-dashboards",
            custom_keys=json.dumps({"since": "2026-01-01"}).encode("utf-8"),
        )
        # --8<-- [end:actionflow-params]

        # ---- Index management ----------------------------------------------
        # --8<-- [start:index]
        # Create an index on a collection, list what's there, drop one.
        cf.data.index.create(collection="housing_stock", index_name="city_1")

        indexes = [ix.name for ix in cf.data.index.get_all(collection="housing_stock").indexes]

        cf.data.index.delete(collection="housing_stock", index_name="city_1")
        # --8<-- [end:index]
        assert "city_1" in indexes

    # ---- App transfer between instances ------------------------------------
    # --8<-- [start:transfer]
    # Move a whole app from one instance to another: export from the source,
    # import into the destination. Each part is bytes, so it passes straight
    # through — no unpacking.
    src = Clappform(location="acme", cluster="prod", api_key="cf_live_...", transport=transport)
    dst = Clappform(location="acme", cluster="qa", api_key="cf_test_...", transport=other_cluster)

    with src, dst:
        bundle = src.client.transfer.export_app(
            id="sales", include_app=True, include_queries=True, include_actionflows=True
        )
        dst.client.transfer.import_app(
            app=bundle.app,
            queries=bundle.queries,
            actionflows=bundle.actionflows,
            overwrite=False,
        )
    # --8<-- [end:transfer]

    # ---- Cross-cluster data copy -------------------------------------------
    # --8<-- [start:cross-cluster]
    # Two clients = two clusters in one process. Read from one, upsert into the
    # other on a business key so re-runs never duplicate.
    prod = Clappform(location="acme", cluster="prod", api_key="cf_live_...", transport=transport)
    qa = Clappform(location="acme", cluster="qa", api_key="cf_test_...", transport=other_cluster)

    with prod, qa:
        data = prod.data.collection("housing_stock").read()
        qa.data.collection("housing_stock").upsert(data, on="address")
    # --8<-- [end:cross-cluster]


# A tiny CSV built in-memory so the ingest recipe runs in CI without a fixture
# file on disk and without an optional file-format dependency. Readers
# substitute their own file bytes (and reader) for the real source.
def _sample_csv() -> bytes:
    return pd.DataFrame(
        [
            {"address": "Prinsengracht 3", "city": "Amsterdam", "energy_label": "B"},
            {"address": "Damrak 70", "city": "Amsterdam", "energy_label": "A"},
        ]
    ).to_csv(index=False).encode("utf-8")


file_bytes = _sample_csv()


if __name__ == "__main__":
    run(build_mock(), build_second_cluster_mock())
