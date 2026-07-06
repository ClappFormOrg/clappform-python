"""Runnable source for the testing-with-LocalMock guide snippets."""

from __future__ import annotations


def run() -> None:
    # --8<-- [start:seed]
    from clappform import Clappform
    from clappform.testing import LocalMock

    # Seed the data plane, then point a client at the mock. No network, no keys
    # that matter — the same JSON codec the real client uses drives the store.
    # `collection("customers")` resolves the slug first, so register the mapping
    # and seed the store under the resolved id.
    mock = LocalMock()
    mock.seed_collection_slug("customers", id="customers-id")
    mock.seed(
        "customers-id",
        [
            {"email": "a@example.com", "plan": "pro"},
            {"email": "b@example.com", "plan": "free"},
        ],
    )
    cf = Clappform(location="acme", cluster="prod", api_key="test", transport=mock)
    # --8<-- [end:seed]

    with cf:
        # --8<-- [start:roundtrip]
        customers = cf.data.collection("customers")

        pro = customers.read(where={"plan": "pro"})
        assert list(pro["email"]) == ["a@example.com"]

        # writes mutate the store, so a follow-up read sees them
        customers.replace_where({"plan": "free"}, {"plan": "pro"})
        assert len(customers.read(where={"plan": "pro"})) == 2
        # --8<-- [end:roundtrip]

        # --8<-- [start:assert-calls]
        # Every call is recorded for assertions.
        assert any(
            call.method.endswith("AggregateStream") for call in mock.calls
        )
        assert mock.calls[-1].location == "acme"
        # --8<-- [end:assert-calls]

    # --8<-- [start:stub]
    # For RPCs without a built-in data handler, register a canned response with
    # .on() keyed by the full gRPC method path — use the RPC's real response
    # message so the stub matches what the server returns. An explicit stub
    # always wins over a built-in handler.
    from clappform.gen.clappform.client.v1.actionflow import actionflow_pb2

    mock.on(
        "/clappform.client.v1.actionflow.ActionflowManagement/Start",
        actionflow_pb2.StartActionflowResponse(message="started", uuid="af-123"),
    )

    with Clappform(location="acme", cluster="prod", api_key="test", transport=mock) as cf:
        started = cf.client.actionflow.start(id="recalculate-dashboards")
        assert started.uuid == "af-123"
    # --8<-- [end:stub]


if __name__ == "__main__":
    run()
