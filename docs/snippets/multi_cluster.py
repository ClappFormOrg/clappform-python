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


if __name__ == "__main__":
    run(build_mock(), build_mock())
