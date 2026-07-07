"""Clappform client construction, discovery wiring, tenancy, and lifecycle."""

import pytest

from clappform import ApiKey, Clappform, ConfigurationError
from clappform import _client as client_mod
from clappform._transport import resolve_endpoints


class FakeTransport:
    def __init__(self) -> None:
        self.calls: list[tuple[str, str | None]] = []

    def invoke(self, kind, method, request, request_cls, response_cls, **options):
        self.calls.append((method, options.get("location")))
        return response_cls()


def make_client(cluster: str = "qa", **kwargs) -> tuple[Clappform, FakeTransport]:
    transport = FakeTransport()
    defaults: dict = {"api_key": "k", "transport": transport}
    defaults.update(kwargs)
    return Clappform("acme", cluster, **defaults), transport


# --- construction validation -------------------------------------------------

def test_requires_location() -> None:
    with pytest.raises(ConfigurationError, match="location"):
        Clappform("", "qa", api_key="k")


def test_requires_exactly_one_credential_source() -> None:
    with pytest.raises(ConfigurationError, match="exactly one"):
        Clappform("acme", "qa")
    with pytest.raises(ConfigurationError, match="exactly one"):
        Clappform("acme", "qa", api_key="k", credentials=ApiKey("x"))


def test_sub_clients_are_wired() -> None:
    cf, _ = make_client()
    for family in ("data", "client", "auth", "notifier"):
        assert hasattr(cf, family)


def test_default_location_injected_and_per_call_override_wins() -> None:
    cf, transport = make_client()
    cf.data.insert.insert_single(collection="orders")
    cf.data.insert.insert_single(collection="orders", location="umbrella")
    assert [loc for _m, loc in transport.calls] == ["acme", "umbrella"]


# --- endpoint resolution ------------------------------------------------------

def test_endpoint_resolution_variants() -> None:
    # Newer clusters serve gRPC on 443, so the address is the bare host and
    # gRPC defaults the secure channel to 443 — no explicit port is appended.
    assert resolve_endpoints("qa")["data"] == "data-qa.clappform.com"
    assert resolve_endpoints("QA-LTS")["client"] == "client-qa-lts.clappform.com"


def test_main_cluster_defaults_to_50051() -> None:
    # The main cluster's gRPC services still listen on :50051, so its defaults
    # carry the port explicitly ("prod" is an alias for the main cluster).
    assert resolve_endpoints("")["data"] == "data.clappform.com:50051"
    assert resolve_endpoints("")["client"] == "client.clappform.com:50051"
    assert resolve_endpoints("prod")["auth"] == "auth.clappform.com:50051"


def test_endpoint_override_wins_and_unknown_family_rejected() -> None:
    # An override is used verbatim (no port appended) and may carry its own
    # host:port — e.g. to point the main cluster at 443, or a local dev endpoint.
    resolved = resolve_endpoints("qa", {"data": "10.0.0.5:50051"})
    assert resolved["data"] == "10.0.0.5:50051"
    assert resolved["auth"] == "auth-qa.clappform.com"
    # Overriding a main-cluster family drops the default :50051 for that family.
    assert resolve_endpoints("", {"client": "client.clappform.com"})["client"] == (
        "client.clappform.com"
    )
    with pytest.raises(ConfigurationError, match="unknown API family"):
        resolve_endpoints("qa", {"nbflow": "x:1"})


# --- cluster discovery wiring -------------------------------------------------

def test_explicit_cluster_never_discovers(monkeypatch: pytest.MonkeyPatch) -> None:
    def boom(location: str) -> str:
        raise AssertionError("discovery must not run for explicit cluster")

    monkeypatch.setattr(client_mod._discovery, "discover_cluster", boom)
    cf, _ = make_client(cluster="qa")
    assert cf.cluster == "qa"
    assert cf.cluster_discovered is False


def test_omitted_cluster_is_discovered(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        client_mod._discovery, "discover_cluster", lambda loc: "prod-lts"
    )
    cf = Clappform("noord-brabant", api_key="k", transport=FakeTransport())
    assert cf.cluster == "prod-lts"
    assert cf.cluster_discovered is True
    assert "(discovered)" in repr(cf)


def test_discovery_failure_propagates_with_hint(monkeypatch: pytest.MonkeyPatch) -> None:
    def fail(location: str) -> str:
        raise ConfigurationError("cluster discovery failed; pass cluster= explicitly")

    monkeypatch.setattr(client_mod._discovery, "discover_cluster", fail)
    with pytest.raises(ConfigurationError, match="pass cluster= explicitly"):
        Clappform("acme", api_key="k", transport=FakeTransport())


# --- with_location ------------------------------------------------------------

def test_with_location_shares_transport_for_explicit_cluster(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        client_mod._discovery,
        "discover_cluster",
        lambda loc: pytest.fail("no discovery for explicit cluster"),
    )
    cf, transport = make_client(cluster="qa")
    clone = cf.with_location("umbrella")
    clone.data.insert.insert_single(collection="orders")
    assert transport.calls == [
        ("/clappform.data.v1.insert.InsertManagement/InsertSingle", "umbrella")
    ]
    assert clone.cluster == "qa"


def test_with_location_same_location_returns_self() -> None:
    cf, _ = make_client()
    assert cf.with_location("acme") is cf


def test_with_location_requires_a_location() -> None:
    cf, _ = make_client()
    with pytest.raises(ConfigurationError, match="location is required"):
        cf.with_location("")


def test_with_location_rediscovers_only_for_discovered_cluster(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    lookups: list[str] = []

    def fake_discover(location: str) -> str:
        lookups.append(location)
        return {"acme": "qa", "umbrella": "qa", "gelderland": ""}[location]

    monkeypatch.setattr(client_mod._discovery, "discover_cluster", fake_discover)
    cf = Clappform("acme", api_key="k", endpoints={"data": "127.0.0.1:1"}, insecure=True)
    try:
        same = cf.with_location("umbrella")  # same cluster -> shared transport
        assert same.cluster == "qa"
        assert same._transport is cf._transport
        other = cf.with_location("gelderland")  # different cluster -> own transport
        assert other.cluster == ""
        assert other.cluster_discovered is True
        assert other._transport is not cf._transport
        assert lookups == ["acme", "umbrella", "gelderland"]
        other.close()
    finally:
        cf.close()


# --- lifecycle ----------------------------------------------------------------

def test_context_manager_closes_owned_transport() -> None:
    closed: list[bool] = []

    class ClosableTransport(FakeTransport):
        def close(self) -> None:
            closed.append(True)

    transport = ClosableTransport()
    with Clappform("acme", "qa", api_key="k", transport=transport):
        pass
    # custom transports are caller-owned: the client must NOT close them
    assert closed == []

    cf = Clappform("acme", "qa", api_key="k", endpoints={"data": "127.0.0.1:1"}, insecure=True)
    cf.close()  # owned transport: close() must not raise, channels torn down


def test_channel_for_rejected_on_custom_transport() -> None:
    cf, _ = make_client()
    with pytest.raises(ConfigurationError, match="custom transport"):
        cf.channel_for("data")


def test_channel_for_returns_live_channel_on_owned_transport() -> None:
    # With an owned GrpcTransport, channel_for exposes the real grpc.Channel and
    # returns the same cached instance on repeat calls.
    import grpc

    cf = Clappform("acme", "qa", api_key="k", endpoints={"data": "127.0.0.1:1"}, insecure=True)
    try:
        channel = cf.channel_for("data")
        assert isinstance(channel, grpc.Channel)
        assert cf.channel_for("data") is channel
    finally:
        cf.close()


def test_with_location_clone_close_does_not_break_parent() -> None:
    # A shared-transport clone is not the transport owner; closing it must be a
    # no-op that leaves the parent (and its channels) usable — the multi-tenant
    # safety invariant.
    cf, transport = make_client(cluster="qa")
    clone = cf.with_location("umbrella")
    clone.close()  # clone does not own the transport
    # parent still serves calls after the clone is closed
    cf.data.insert.insert_single(collection="orders")
    assert transport.calls[-1][1] == "acme"
