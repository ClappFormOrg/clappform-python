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
    assert resolve_endpoints("qa")["data"] == "data-qa.clappform.com:443"
    assert resolve_endpoints("")["data"] == "data.clappform.com:443"
    assert resolve_endpoints("prod")["auth"] == "auth.clappform.com:443"
    assert resolve_endpoints("QA-LTS")["client"] == "client-qa-lts.clappform.com:443"


def test_endpoint_override_wins_and_unknown_family_rejected() -> None:
    resolved = resolve_endpoints("qa", {"data": "10.0.0.5:50051"})
    assert resolved["data"] == "10.0.0.5:50051"
    assert resolved["auth"] == "auth-qa.clappform.com:443"
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
