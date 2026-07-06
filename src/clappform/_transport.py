"""gRPC transport: endpoint resolution, channels, retries, and the Caller.

The generated service layer talks to a :class:`~clappform._runtime.Caller`;
:class:`GrpcTransport` is the production implementation. It owns one lazily
created channel per endpoint, composes per-call metadata (credentials +
tenant location + caller extras), applies the default deadline, and
translates every ``grpc.RpcError`` into the typed hierarchy — including
errors raised mid-iteration on streaming responses.
"""

from __future__ import annotations

import threading
from collections.abc import Iterator
from dataclasses import dataclass, field
from typing import Any

import grpc

from clappform._auth import Credentials
from clappform._errors import ConfigurationError, translate_rpc_error
from clappform._runtime import CallKind

BASE_DOMAIN = "clappform.com"

# Host prefix per API family, forming {prefix}{-extension}.clappform.com.
# The authoriser serves under "auth", matching its family alias.
HOST_PREFIXES = {
    "data": "data",
    "client": "client",
    "auth": "auth",
    "notifier": "notifier",
}

# Package segment -> family alias, mirroring the generated service layer.
_PACKAGE_FAMILIES = {"authoriser": "auth"}


@dataclass(frozen=True)
class RetryPolicy:
    """Retry configuration applied through gRPC's built-in retry support."""

    max_attempts: int = 4
    initial_backoff: str = "0.2s"
    max_backoff: str = "2s"
    backoff_multiplier: float = 2.0
    retryable_status_codes: tuple[str, ...] = ("UNAVAILABLE",)

    def service_config(self) -> str:
        import json

        return json.dumps(
            {
                "methodConfig": [
                    {
                        "name": [{}],
                        "retryPolicy": {
                            "maxAttempts": self.max_attempts,
                            "initialBackoff": self.initial_backoff,
                            "maxBackoff": self.max_backoff,
                            "backoffMultiplier": self.backoff_multiplier,
                            "retryableStatusCodes": list(self.retryable_status_codes),
                        },
                    }
                ]
            }
        )


DEFAULT_RETRIES = RetryPolicy()

_BASE_CHANNEL_OPTIONS: list[tuple[str, Any]] = [
    ("grpc.keepalive_time_ms", 30_000),
    ("grpc.keepalive_timeout_ms", 10_000),
    ("grpc.keepalive_permit_without_calls", 1),
    ("grpc.max_send_message_length", 64 * 1024 * 1024),
    ("grpc.max_receive_message_length", 64 * 1024 * 1024),
]


def resolve_endpoints(
    cluster: str,
    overrides: dict[str, str] | None = None,
) -> dict[str, str]:
    """Build the per-family endpoint map for a cluster extension.

    ``cluster`` is the host extension: ``""`` (or ``"prod"``) for the main
    cluster, ``"qa"``-style values otherwise. The supported (current) clusters
    serve gRPC over TLS on 443, so the address is the bare host with no port —
    gRPC defaults a secure channel to 443. Explicit ``overrides`` win per family
    and may carry their own ``host:port`` (e.g. for an older cluster still on
    ``:50051`` or a local dev endpoint).
    """
    extension = cluster.strip().lstrip("-").lower()
    if extension == "prod":
        extension = ""
    suffix = f"-{extension}" if extension else ""
    endpoints = {
        family: f"{prefix}{suffix}.{BASE_DOMAIN}"
        for family, prefix in HOST_PREFIXES.items()
    }
    for family, address in (overrides or {}).items():
        if family not in endpoints:
            raise ConfigurationError(
                f"unknown API family {family!r} in endpoints=; "
                f"expected one of {sorted(endpoints)}"
            )
        endpoints[family] = address
    return endpoints


def family_of_method(method: str) -> str:
    """'/clappform.data.v1.insert.InsertManagement/InsertMany' -> 'data'."""
    package = method.lstrip("/").split("/", 1)[0]
    parts = package.split(".")
    if len(parts) < 2 or parts[0] != "clappform":
        raise ConfigurationError(f"cannot derive API family from method {method!r}")
    segment = parts[1]
    return _PACKAGE_FAMILIES.get(segment, segment)


@dataclass
class GrpcTransport:
    """Production Caller: channels, metadata, deadlines, error translation."""

    endpoints: dict[str, str]
    credentials: Credentials
    cluster: str
    insecure: bool = False
    default_timeout: float | None = 60.0
    retries: RetryPolicy | None = DEFAULT_RETRIES
    channel_options: list[tuple[str, Any]] | None = None

    _channels: dict[str, grpc.Channel] = field(default_factory=dict, init=False, repr=False)
    _lock: threading.Lock = field(default_factory=threading.Lock, init=False, repr=False)
    _closed: bool = field(default=False, init=False, repr=False)

    def _options(self) -> list[tuple[str, Any]]:
        options = list(_BASE_CHANNEL_OPTIONS)
        if self.retries is not None:
            options.append(("grpc.enable_retries", 1))
            options.append(("grpc.service_config", self.retries.service_config()))
        if self.channel_options:
            options.extend(self.channel_options)
        return options

    def channel_for(self, family: str) -> grpc.Channel:
        try:
            address = self.endpoints[family]
        except KeyError:
            raise ConfigurationError(
                f"no endpoint configured for API family {family!r}"
            ) from None
        with self._lock:
            if self._closed:
                raise ConfigurationError("client is closed")
            channel = self._channels.get(address)
            if channel is None:
                if self.insecure:
                    channel = grpc.insecure_channel(address, options=self._options())
                else:
                    channel = grpc.secure_channel(
                        address, grpc.ssl_channel_credentials(), options=self._options()
                    )
                self._channels[address] = channel
            return channel

    def close(self) -> None:
        with self._lock:
            self._closed = True
            channels, self._channels = list(self._channels.values()), {}
        for channel in channels:
            channel.close()

    def _metadata(
        self,
        location: str | None,
        extra: tuple[tuple[str, str], ...] | None,
    ) -> tuple[tuple[str, str], ...]:
        metadata = list(self.credentials.metadata_for_call())
        if location:
            metadata.append(("location", location))
        if extra:
            metadata.extend(extra)
        return tuple(metadata)

    def invoke(
        self,
        kind: CallKind,
        method: str,
        request: Any,
        request_cls: Any,  # protobuf message class (SerializeToString/FromString)
        response_cls: Any,
        *,
        timeout: float | None = None,
        metadata: tuple[tuple[str, str], ...] | None = None,
        location: str | None = None,
    ) -> Any:
        family = family_of_method(method)
        channel = self.channel_for(family)
        multicallable = getattr(channel, kind)(
            method,
            request_serializer=request_cls.SerializeToString,
            response_deserializer=response_cls.FromString,
        )
        call_kwargs = {
            "timeout": timeout if timeout is not None else self.default_timeout,
            "metadata": self._metadata(location, metadata),
        }
        context = {"method": method, "cluster": self.cluster, "location": location}
        try:
            result = multicallable(request, **call_kwargs)
        except grpc.RpcError as exc:
            raise translate_rpc_error(exc, **context) from exc
        if kind.endswith("_stream"):
            return self._translating_iterator(result, context)
        return result

    @staticmethod
    def _translating_iterator(stream: Any, context: dict[str, Any]) -> Iterator[Any]:
        try:
            yield from stream
        except grpc.RpcError as exc:
            raise translate_rpc_error(exc, **context) from exc
