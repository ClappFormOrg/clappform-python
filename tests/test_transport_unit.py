"""Transport internals exercised directly (no wire).

`test_transport_grpc.py` drives the full stack over a real loopback channel;
this file covers the branches that end-to-end tests can't easily reach: the
production TLS channel construction, the channel_for guard/cache paths, the
`_options`/`_metadata` composition, and `family_of_method` parsing.
"""

from __future__ import annotations

import grpc
import pytest

from clappform import ApiKey, ConfigurationError
from clappform._transport import (
    DEFAULT_RETRIES,
    GrpcTransport,
    RetryPolicy,
    family_of_method,
)


def _transport(**overrides) -> GrpcTransport:
    defaults = dict(
        endpoints={"data": "data.clappform.com"},
        credentials=ApiKey("k"),
        cluster="",
    )
    defaults.update(overrides)
    return GrpcTransport(**defaults)  # type: ignore[arg-type]


# --- family_of_method --------------------------------------------------------

def test_family_of_method_derives_family() -> None:
    assert (
        family_of_method("/clappform.data.v1.insert.InsertManagement/InsertMany")
        == "data"
    )


def test_family_of_method_maps_authoriser_to_auth() -> None:
    # The authoriser package is served under the `auth` family alias.
    assert family_of_method("/clappform.authoriser.v1.apikey.APIKeyManagement/Generate") == "auth"


@pytest.mark.parametrize("method", ["/foo.bar/Baz", "/clappform/X", "NoSlashes"])
def test_family_of_method_rejects_malformed(method: str) -> None:
    with pytest.raises(ConfigurationError, match="cannot derive API family"):
        family_of_method(method)


# --- channel_for -------------------------------------------------------------

def test_channel_for_uses_secure_channel_by_default(monkeypatch) -> None:
    # Production default is insecure=False; the secure/TLS path must be taken.
    # (Every wire test uses insecure=True, so this branch is otherwise unrun.)
    calls: dict[str, object] = {}

    def fake_secure(address, creds, options=None):
        calls["address"] = address
        calls["creds"] = creds
        calls["options"] = options
        return "SECURE_CHANNEL"

    monkeypatch.setattr(grpc, "secure_channel", fake_secure)
    monkeypatch.setattr(grpc, "ssl_channel_credentials", lambda: "SSL_CREDS")

    transport = _transport(insecure=False)
    channel = transport.channel_for("data")

    assert channel == "SECURE_CHANNEL"
    assert calls["address"] == "data.clappform.com"
    assert calls["creds"] == "SSL_CREDS"


def test_channel_for_uses_insecure_channel_when_requested(monkeypatch) -> None:
    monkeypatch.setattr(grpc, "insecure_channel", lambda address, options=None: "INSECURE")
    transport = _transport(insecure=True)
    assert transport.channel_for("data") == "INSECURE"


def test_channel_for_caches_one_channel_per_address(monkeypatch) -> None:
    made: list[str] = []
    monkeypatch.setattr(
        grpc, "insecure_channel", lambda address, options=None: made.append(address) or object()
    )
    transport = _transport(insecure=True)
    first = transport.channel_for("data")
    second = transport.channel_for("data")
    assert first is second  # cache hit, not rebuilt
    assert made == ["data.clappform.com"]  # channel built exactly once


def test_channel_for_unknown_family_raises(monkeypatch) -> None:
    monkeypatch.setattr(grpc, "insecure_channel", lambda address, options=None: object())
    transport = _transport(insecure=True)  # only "data" is configured
    with pytest.raises(ConfigurationError, match="no endpoint configured"):
        transport.channel_for("notifier")


def test_channel_for_after_close_raises(monkeypatch) -> None:
    monkeypatch.setattr(grpc, "insecure_channel", lambda address, options=None: object())
    transport = _transport(insecure=True)
    transport.close()
    with pytest.raises(ConfigurationError, match="client is closed"):
        transport.channel_for("data")


def test_close_is_idempotent_and_tears_down_channels(monkeypatch) -> None:
    class FakeChannel:
        def __init__(self) -> None:
            self.closed = 0

        def close(self) -> None:
            self.closed += 1

    channels: list[FakeChannel] = []
    monkeypatch.setattr(
        grpc,
        "insecure_channel",
        lambda address, options=None: channels.append(FakeChannel()) or channels[-1],
    )
    transport = _transport(insecure=True)
    ch = transport.channel_for("data")
    transport.close()
    transport.close()  # second close must not raise
    assert ch.closed == 1


# --- _options ----------------------------------------------------------------

def test_options_include_custom_channel_options() -> None:
    transport = _transport(channel_options=[("grpc.custom_opt", 7)])
    assert ("grpc.custom_opt", 7) in transport._options()


def test_options_include_retries_by_default() -> None:
    transport = _transport(retries=DEFAULT_RETRIES)
    keys = [k for k, _ in transport._options()]
    assert "grpc.enable_retries" in keys
    assert "grpc.service_config" in keys


def test_options_omit_retries_when_disabled() -> None:
    transport = _transport(retries=None)
    keys = [k for k, _ in transport._options()]
    assert "grpc.enable_retries" not in keys


# --- _metadata ---------------------------------------------------------------

def test_metadata_includes_credentials_and_location() -> None:
    transport = _transport()
    md = dict(transport._metadata("acme", None))
    assert md["x-api-key"] == "k"
    assert md["location"] == "acme"


def test_metadata_omits_location_header_when_none() -> None:
    transport = _transport()
    md = dict(transport._metadata(None, None))
    assert "location" not in md


def test_metadata_appends_per_call_extra() -> None:
    transport = _transport()
    md = transport._metadata("acme", (("x-trace-id", "abc"),))
    assert ("x-trace-id", "abc") in md


def test_retry_policy_service_config_defaults() -> None:
    # DEFAULT_RETRIES values flow into the gRPC service config JSON.
    cfg = RetryPolicy().service_config()
    assert '"maxAttempts": 4' in cfg
    assert "UNAVAILABLE" in cfg
