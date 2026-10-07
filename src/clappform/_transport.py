"""gRPC transport: endpoint resolution, channels, retries, and the Caller.

The generated service layer talks to a :class:`~clappform._runtime.Caller`;
:class:`GrpcTransport` is the production implementation. It owns one lazily
created channel per endpoint, composes per-call metadata (credentials +
tenant location + caller extras), applies the default deadline, and
translates every ``grpc.RpcError`` into the typed hierarchy, including
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
# Two families are served from a host that doesn't match their alias: the
# authoriser family ("auth") lives on the "login" host (co-located with data on
# the cluster gateway, e.g. login.clappform.com), and the notifier family lives
# on "notify" (notify.clappform.com). The literal "auth."/"notifier." hosts
# point at a separate, unreachable box. The rest match their family alias.
HOST_PREFIXES = {
    "data": "data",
    "client": "client",
    "auth": "login",
    "notifier": "notify",
}

# Package segment -> family alias, mirroring the generated service layer.
_PACKAGE_FAMILIES = {"authoriser": "auth"}


# Data-plane services whose RPCs write. gRPC retries an UNAVAILABLE call even
# when the server already applied it, so a retried InsertMany can duplicate
# rows. These services get no retry policy; gRPC's transparent retries (the
# request never reached the server) still apply to them.
NON_RETRIED_SERVICES = (
    "clappform.data.v1.insert.InsertManagement",
    "clappform.data.v1.update.UpdateManagement",
    "clappform.data.v1.sync.SyncManagement",
    "clappform.data.v1.delete.DeleteManagement",
)


def _duration(value: float | str) -> str:
    """Seconds as a float, or an already-formatted ``"0.2s"`` string."""
    if isinstance(value, str):
        return value
    return f"{value:.9f}".rstrip("0").rstrip(".") + "s"


def _seconds(value: float | str) -> float:
    return float(value[:-1]) if isinstance(value, str) else float(value)


@dataclass(frozen=True)
class RetryPolicy:
    """Retry configuration applied through gRPC's built-in retry support.

    Backoffs are seconds (``0.2``); the ``"0.2s"`` string form is also
    accepted. gRPC caps ``max_attempts`` at 5, so larger values are rejected
    rather than silently clamped. The policy covers every RPC except the
    data-plane writes in :data:`NON_RETRIED_SERVICES`, which may have been
    applied before the failure.
    """

    max_attempts: int = 4
    initial_backoff: float | str = 0.2
    max_backoff: float | str = 2.0
    backoff_multiplier: float = 2.0
    retryable_status_codes: tuple[str, ...] = ("UNAVAILABLE",)

    def __post_init__(self) -> None:
        if not 2 <= self.max_attempts <= 5:
            raise ConfigurationError(
                f"RetryPolicy.max_attempts must be between 2 and 5, got {self.max_attempts}; "
                f"pass retries=None to disable retries"
            )
        try:
            backoffs = (_seconds(self.initial_backoff), _seconds(self.max_backoff))
        except ValueError:
            raise ConfigurationError(
                "RetryPolicy backoffs must be seconds, e.g. 0.2 or '0.2s'"
            ) from None
        if min(backoffs) <= 0 or self.backoff_multiplier <= 0:
            raise ConfigurationError("RetryPolicy backoffs and multiplier must be positive")
        if not self.retryable_status_codes:
            raise ConfigurationError("RetryPolicy.retryable_status_codes must not be empty")

    def service_config(self) -> str:
        import json

        return json.dumps(
            {
                "methodConfig": [
                    {
                        "name": [{}],
                        "retryPolicy": {
                            "maxAttempts": self.max_attempts,
                            "initialBackoff": _duration(self.initial_backoff),
                            "maxBackoff": _duration(self.max_backoff),
                            "backoffMultiplier": self.backoff_multiplier,
                            "retryableStatusCodes": list(self.retryable_status_codes),
                        },
                    },
                    # A service-level entry is more specific than the default
                    # above, so these services run with no retry policy.
                    {"name": [{"service": service} for service in NON_RETRIED_SERVICES]},
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
    cluster, ``"qa"``-style values otherwise. The newer clusters serve gRPC
    over TLS on 443, so their address is the bare host with no port, because gRPC
    defaults a secure channel to 443. The main cluster still listens on
    ``:50051``, so its defaults carry that port explicitly. Explicit
    ``overrides`` win per family and are used verbatim (no port is appended),
    so an override may carry its own ``host:port``, e.g. to point the main
    cluster at 443 once it migrates, or at a local dev endpoint.
    """
    extension = cluster.strip().lstrip("-").lower()
    if extension == "prod":
        extension = ""
    suffix = f"-{extension}" if extension else ""
    # The main cluster's gRPC services are still on :50051; every other cluster
    # has moved to TLS on 443 (gRPC's secure-channel default, so no port).
    port = ":50051" if extension == "" else ""
    endpoints = {
        family: f"{prefix}{suffix}.{BASE_DOMAIN}{port}"
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
    cluster_discovered: bool = False
    insecure: bool = False
    default_timeout: float | None = 60.0
    stream_timeout: float | None = None
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
        if timeout is None:
            # A unary call gets the client-wide deadline. A streaming call runs
            # as long as it keeps moving (keepalive detects a dead connection),
            # because one deadline covers the whole stream, including the time
            # the caller spends between chunks.
            timeout = self.default_timeout if kind == "unary_unary" else self.stream_timeout
        call_kwargs = {
            "timeout": timeout,
            "metadata": self._metadata(location, metadata),
        }
        context: dict[str, Any] = {
            "method": method,
            "cluster": self.cluster,
            "cluster_discovered": self.cluster_discovered,
            "location": location,
        }
        feed = _RequestFeed(request) if kind.startswith("stream") else None
        try:
            result = multicallable(request if feed is None else feed, **call_kwargs)
        except grpc.RpcError as exc:
            raise _failure(exc, feed, context) from exc
        if kind.endswith("_stream"):
            return self._translating_iterator(result, context, feed)
        return result

    @staticmethod
    def _translating_iterator(
        stream: Any, context: dict[str, Any], feed: _RequestFeed | None
    ) -> Iterator[Any]:
        try:
            yield from stream
        except grpc.RpcError as exc:
            raise _failure(exc, feed, context) from exc
        finally:
            # A caller that stops iterating early (break, an exception, a
            # dropped generator) must not leave the call open on the server.
            # Cancelling a finished call is a no-op.
            cancel = getattr(stream, "cancel", None)
            if cancel is not None:
                cancel()


class _RequestFeed:
    """A stream-input request iterator that remembers why it failed.

    gRPC consumes request iterators on its own thread. When producing a request
    raises (a bad item, a caller's ``progress`` callback, a codec error), gRPC
    logs it and cancels the call, so the caller would only see CANCELLED.
    Keeping the exception lets :func:`_failure` re-raise the real cause.
    """

    __slots__ = ("_requests", "error")

    def __init__(self, requests: Any) -> None:
        self._requests = iter(requests)
        self.error: BaseException | None = None

    def __iter__(self) -> _RequestFeed:
        return self

    def __next__(self) -> Any:
        try:
            return next(self._requests)
        except StopIteration:
            raise
        except BaseException as exc:
            self.error = exc
            raise


def _failure(
    error: grpc.RpcError, feed: _RequestFeed | None, context: dict[str, Any]
) -> BaseException:
    """The exception to raise for a failed call: the request side's own error
    when producing a request is what broke the call, otherwise the typed
    translation of the gRPC status."""
    if feed is not None and feed.error is not None:
        return feed.error
    return translate_rpc_error(error, **context)
