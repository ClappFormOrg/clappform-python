"""Runnable source for the multi-cluster / multi-tenant guide snippets."""

from __future__ import annotations

from clappform.testing import LocalMock


def build_mock() -> LocalMock:
    mock = LocalMock()
    mock.seed_collection_slug("orders", id="orders-id")
    mock.seed("orders-id", [{"order_id": "A-1", "amount": 120.0, "region": "EU"}])
    return mock


def run(prod_transport: LocalMock, qa_transport: LocalMock) -> None:
    # --8<-- [start:two-clusters]
    from clappform import Clappform

    # Two clusters, one process, nothing global. The `cluster` extension picks
    # the endpoints (prod -> data.clappform.com, qa -> data-qa.clappform.com);
    # `location` picks the tenant within them. Credentials are per client.
    prod = Clappform(cluster="prod", location="acme", api_key="cf_live_prod_...")
    qa = Clappform(cluster="qa", location="acme", api_key="cf_live_qa_...")
    # --8<-- [end:two-clusters]

    prod = Clappform(cluster="prod", location="acme", api_key="x", transport=prod_transport)
    qa = Clappform(cluster="qa", location="acme", api_key="x", transport=qa_transport)

    imported: dict[str, bytes] = {}
    _register_transfer_stubs(prod_transport, qa_transport, imported)

    with prod, qa:
        # --8<-- [start:cross-cluster]
        # Pull from prod, mirror into qa by business key.
        df = prod.data.collection("orders").read()
        qa.data.collection("orders").upsert(df, on="order_id")
        # --8<-- [end:cross-cluster]
        assert len(df) == 1
        # the row was mirrored into the qa cluster's store
        assert len(qa_transport.records("orders-id")) == 1

        # --8<-- [start:with-location]
        # Same cluster, another tenant: with_location() clones cheaply and
        # shares the underlying connections — only the tenant metadata differs.
        beta = prod.with_location("beta")
        beta_orders = beta.data.collection("orders").read()
        # --8<-- [end:with-location]
        # the clone shares prod's transport, so it reads prod's seeded row
        assert len(beta_orders) == 1

        # --8<-- [start:transfer-app]
        # Move a whole app — its collections, and optionally its queries,
        # actionflows and questionnaires — from one instance to another.
        # export_app() reads the bundle from the source; import_app() writes it
        # into the target. The AppExport's four byte blobs are exactly the
        # fields import_app() consumes, so the hand-off needs no reshaping.
        bundle = prod.client.transfer.export_app(
            id="sales-dashboard",
            include_app=True,
            include_queries=True,
            include_actionflows=True,
            include_questionnaires=True,
        )

        qa.client.transfer.import_app(
            app=bundle.app,
            queries=bundle.queries,
            actionflows=bundle.actionflows,
            questionnaires=bundle.questionnaires,
            overwrite=False,  # refuse to clobber an app already on the target
        )
        # --8<-- [end:transfer-app]
        # the exact blobs exported from prod reached qa's import handler intact
        assert imported == {
            "app": b"<app-bundle>",
            "queries": b"<queries-bundle>",
            "actionflows": b"<actionflows-bundle>",
            "questionnaires": b"<questionnaires-bundle>",
        }


def _register_transfer_stubs(
    source: LocalMock, target: LocalMock, captured: dict[str, bytes]
) -> None:
    """Stub ExportApp on the source and ImportApp on the target.

    Transfer RPCs are not data-plane calls, so LocalMock has no built-in
    handler — the same ``.on()`` stubbing you'd use in your own tests. The
    import stub is a handler that captures the received blobs so the snippet
    can assert the bundle crossed instances intact.
    """
    from clappform.gen.clappform.client.v1.transfer import transfer_pb2
    from clappform.gen.clappform.v1.commons import commons_pb2

    source.on(
        "/clappform.client.v1.transfer.TransferManagement/ExportApp",
        transfer_pb2.AppExport(
            app=b"<app-bundle>",
            queries=b"<queries-bundle>",
            actionflows=b"<actionflows-bundle>",
            questionnaires=b"<questionnaires-bundle>",
        ),
    )

    def _capture_import(request: transfer_pb2.AppImport) -> commons_pb2.Message:
        captured.update(
            app=request.app,
            queries=request.queries,
            actionflows=request.actionflows,
            questionnaires=request.questionnaires,
        )
        return commons_pb2.Message(message="app imported")

    target.on("/clappform.client.v1.transfer.TransferManagement/ImportApp", _capture_import)


if __name__ == "__main__":
    run(build_mock(), build_mock())
