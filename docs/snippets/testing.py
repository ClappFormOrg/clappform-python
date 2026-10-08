"""Runnable source for the testing-with-LocalMock guide snippets."""

from __future__ import annotations

import pytest


def run() -> None:
    # --8<-- [start:seed]
    from clappform import Clappform
    from clappform.testing import LocalMock

    # Seed the data plane, then point a client at the mock. No network, no keys
    # that matter; the same JSON codec the real client uses drives the store.
    # `collection("customers")` resolves the slug first, so register the mapping
    # and seed the store under the resolved id.
    mock = LocalMock()
    mock.seed_collection_slug("customers", id="customers-id")
    mock.seed(
        "customers-id",
        [
            {"email": "a@example.com", "plan": "pro", "seats": 5},
            {"email": "b@example.com", "plan": "free", "seats": 1},
        ],
    )
    cf = Clappform(location="acme", api_key="test", transport=mock)
    # --8<-- [end:seed]

    with cf:
        # --8<-- [start:roundtrip]
        customers = cf.data.collection("customers")

        pro = customers.read(
            pipeline=[{"$match": {"plan": "pro", "seats": {"$gte": 2}}}, {"$sort": {"email": 1}}]
        )
        assert list(pro["email"]) == ["a@example.com"]

        # writes mutate the store, so a follow-up read sees them
        free = customers.read(pipeline=[{"$match": {"plan": "free"}}])
        free["plan"] = "pro"
        customers.upsert(free.drop(columns="_id"), on="email")
        assert len(customers.read(pipeline=[{"$match": {"plan": "pro"}}])) == 2

        # records() returns a copy of the store for direct assertions
        assert {row["plan"] for row in mock.records("customers-id")} == {"pro"}
        # --8<-- [end:roundtrip]

        # --8<-- [start:assert-calls]
        # Every call is recorded for assertions.
        assert any(
            call.method.endswith("AggregateStream") for call in mock.calls
        )
        assert mock.calls[-1].location == "acme"
        # --8<-- [end:assert-calls]

    # --8<-- [start:unreleased]
    from clappform import NotSupportedError

    # By default the mock answers the RPCs the Data Connector does not serve
    # yet (update, update_where, delete(where=)) the way a real cluster does.
    with (
        Clappform(location="acme", api_key="test", transport=mock) as cf,
        pytest.raises(NotSupportedError),
    ):
        cf.data.collection("customers").update_where({"plan": "pro"}, {"seats": 10})

    # include_unreleased=True emulates them, to test code written ahead of
    # the server rollout.
    ahead = LocalMock(include_unreleased=True)
    ahead.seed_collection_slug("customers", id="customers-id")
    ahead.seed("customers-id", mock.records("customers-id"))
    with Clappform(location="acme", api_key="test", transport=ahead) as cf:
        cf.data.collection("customers").update_where({"plan": "pro"}, {"seats": 10})
    assert {row["seats"] for row in ahead.records("customers-id")} == {10}
    # --8<-- [end:unreleased]

    # --8<-- [start:saved-query]
    # seed_query registers a saved query by name, backed by a seeded
    # collection, so cf.data.query(name) resolves and reads with no server.
    mock.seed_query("all-customers", collection="customers-id")
    with Clappform(location="acme", api_key="test", transport=mock) as cf:
        assert len(cf.data.query("all-customers").read()) == 2
    # --8<-- [end:saved-query]

    # --8<-- [start:stub]
    # For RPCs without a built-in data handler, register a canned response with
    # .on() keyed by the full gRPC method path; use the RPC's real response
    # message so the stub matches what the server returns. An explicit stub
    # always wins over a built-in handler.
    from clappform.gen.clappform.client.v1.actionflow import actionflow_pb2

    mock.on(
        "/clappform.client.v1.actionflow.ActionflowManagement/Start",
        actionflow_pb2.StartActionflowResponse(message="started", uuid="af-123"),
    )

    with Clappform(location="acme", api_key="test", transport=mock) as cf:
        started = cf.client.actionflow.start(id="recalculate-dashboards")
        assert started.uuid == "af-123"
    # --8<-- [end:stub]

    # --8<-- [start:stub-error]
    from clappform import NotFoundError, TransientError

    # A handler stub receives the request and may raise, so a test can drive
    # the error paths. Raise the client's own exception types with the status
    # the server would send.
    def missing_flow(request):
        raise NotFoundError(f"no actionflow {request.id!r}", status="NOT_FOUND")

    mock.on("/clappform.client.v1.actionflow.ActionflowManagement/Start", missing_flow)

    def unavailable(requests):
        raise TransientError("connection reset", status="UNAVAILABLE")

    mock.on("/clappform.data.v1.insert.InsertManagement/InsertMany", unavailable)

    with Clappform(location="acme", api_key="test", transport=mock) as cf:
        with pytest.raises(NotFoundError):
            cf.client.actionflow.start(id="nope")
        with pytest.raises(TransientError) as failure:
            import pandas as pd

            cf.data.collection("customers").append(pd.DataFrame([{"email": "c@example.com"}]))
        assert failure.value.rows_written == 0
    # --8<-- [end:stub-error]

    # --8<-- [start:reset]
    # reset() clears recorded calls, stubs, seeded collections and listings,
    # so one mock can serve several independent tests.
    mock.reset()
    assert mock.calls == [] and mock.records("customers-id") == []
    # --8<-- [end:reset]


if __name__ == "__main__":
    run()
