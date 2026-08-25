"""Runnable source for the actionflows-&-listings guide snippets.

These operations live on ``cf.client`` (not the DataFrame handle): starting an
actionflow, and listing collections, apps, saved queries and cronjobs. None of
them are data-plane RPCs, so ``LocalMock`` has no built-in handler; each is
backed by an explicit ``.on()`` stub keyed on the full gRPC method path, which
is exactly how you'd stub them in your own tests. Runs against ``LocalMock`` in
CI so the guide's code matches the client.
"""

from __future__ import annotations

from clappform.testing import LocalMock


def build_mock() -> LocalMock:
    from clappform.gen.clappform.client.v1.actionflow import actionflow_pb2
    from clappform.gen.clappform.client.v1.app import app_pb2
    from clappform.gen.clappform.client.v1.collection import collection_pb2
    from clappform.gen.clappform.client.v1.cronjob import cronjob_pb2
    from clappform.gen.clappform.client.v1.query import query_pb2
    from clappform.gen.clappform.v1.commons import commons_pb2

    def one_page(*items: object) -> commons_pb2.Pagination:
        # A single-page listing: pages == page terminates iter_get_all's loop.
        return commons_pb2.Pagination(page=1, pages=1, total=len(items))

    mock = LocalMock()

    # Starting an actionflow returns the run's uuid so you can track it.
    mock.on(
        "/clappform.client.v1.actionflow.ActionflowManagement/Start",
        actionflow_pb2.StartActionflowResponse(message="started", uuid="run-abc123"),
    )
    # A one-page listing of actionflows.
    mock.on(
        "/clappform.client.v1.actionflow.ActionflowManagement/GetAll",
        actionflow_pb2.Actionflows(
            actionflows=[
                actionflow_pb2.Actionflow(id="af-1", name="recalculate-dashboards"),
                actionflow_pb2.Actionflow(id="af-2", name="nightly-export"),
            ],
            pagination=one_page("af-1", "af-2"),
        ),
    )
    # Listing collections, apps, saved queries and cronjobs.
    mock.on(
        "/clappform.client.v1.collection.CollectionManagement/GetAll",
        collection_pb2.Collections(
            collections=[
                collection_pb2.Collection(id="c-1", slug="sales_orders"),
                collection_pb2.Collection(id="c-2", slug="customers"),
            ],
            pagination=one_page("c-1", "c-2"),
        ),
    )
    mock.on(
        "/clappform.client.v1.app.AppManagement/GetAll",
        app_pb2.Apps(
            apps=[app_pb2.App(id="a-1", slug="sales"), app_pb2.App(id="a-2", slug="ops")],
            pagination=one_page("a-1", "a-2"),
        ),
    )
    mock.on(
        "/clappform.client.v1.query.QueryManagement/GetAll",
        query_pb2.Queries(
            queries=[query_pb2.Query(id="q-1", name="monthly-revenue-per-region")],
            pagination=one_page("q-1"),
        ),
    )
    mock.on(
        "/clappform.client.v1.cronjob.CronjobManagement/GetAll",
        cronjob_pb2.Cronjobs(
            cronjobs=[cronjob_pb2.Cronjob(id="cj-1", name="nightly-sync", pattern="0 2 * * *")],
            pagination=one_page("cj-1"),
        ),
    )
    return mock


def run(transport: LocalMock) -> None:
    from clappform import Clappform

    cf = Clappform(location="acme", cluster="prod", api_key="cf_live_...", transport=transport)

    with cf:
        # --8<-- [start:start-actionflow]
        # Trigger an actionflow by id. The response carries the run's uuid, so
        # you can correlate it with the tasks it spawns.
        started = cf.client.actionflow.start(id="recalculate-dashboards")
        run_id = started.uuid
        # --8<-- [end:start-actionflow]
        assert run_id == "run-abc123"

        # --8<-- [start:list-actionflows]
        # iter_get_all() auto-paginates: it yields every actionflow across all
        # pages, so you never manage `page` yourself.
        for actionflow in cf.client.actionflow.iter_get_all():
            handle(actionflow.name)

        # Or take one page at a time when you want the pagination metadata.
        page = cf.client.actionflow.get_all(limit=50)
        total = page.pagination.total
        # --8<-- [end:list-actionflows]
        assert total == 2

        # --8<-- [start:list-collections]
        # Read every collection in the tenant. Each Collection carries its slug
        # and id, the same id cf.data.collection(slug) resolves to
        # internally, so this is how you discover what's there to read.
        collections = list(cf.client.collection.iter_get_all())
        slugs = [c.slug for c in collections]
        # --8<-- [end:list-collections]
        assert slugs == ["sales_orders", "customers"]

        # --8<-- [start:list-others]
        # The same get_all / iter_get_all pair lists apps, saved queries and
        # cronjobs; anything on cf.client with a listing follows this shape.
        apps = list(cf.client.app.iter_get_all())
        queries = list(cf.client.query.iter_get_all())
        cronjobs = list(cf.client.cronjob.iter_get_all())
        # --8<-- [end:list-others]
        assert [a.slug for a in apps] == ["sales", "ops"]
        assert [q.name for q in queries] == ["monthly-revenue-per-region"]
        assert [c.name for c in cronjobs] == ["nightly-sync"]


def handle(name: str) -> None:
    """Stand-in for whatever the caller does with each item."""
    assert isinstance(name, str)


if __name__ == "__main__":
    run(build_mock())
