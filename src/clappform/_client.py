"""The Clappform client: one instance = one (cluster, location, credentials)
binding.

Nothing is global — two instances pointed at two clusters coexist in one
process, and :meth:`Clappform.with_location` gives a cheap same-cluster
clone for another tenant, sharing connections and configuration.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from clappform import _discovery, _resolve, _runtime, dataframes
from clappform._auth import ApiKey, Credentials
from clappform._errors import ConfigurationError
from clappform._transport import (
    DEFAULT_RETRIES,
    GrpcTransport,
    RetryPolicy,
    resolve_endpoints,
)
from clappform.services import API_FAMILIES

if TYPE_CHECKING:
    from clappform.services.auth import AuthAPI
    from clappform.services.client import ClientAPI
    from clappform.services.data import DataAPI
    from clappform.services.notifier import NotifierAPI


class _BoundCaller:
    """Caller that injects an instance's default tenant location.

    Per-call ``location=`` overrides still win; everything else is passed
    straight through to the underlying transport (or test double).
    """

    __slots__ = ("_inner", "_location")

    def __init__(self, inner: _runtime.Caller, location: str) -> None:
        self._inner = inner
        self._location = location

    def invoke(self, kind, method, request, request_cls, response_cls, **options):
        if options.get("location") is None:
            options["location"] = self._location
        return self._inner.invoke(
            kind, method, request, request_cls, response_cls, **options
        )


class Clappform:
    """Client for every Clappform API on one cluster, bound to one tenant.

    ``cluster`` is the host extension (``"qa"``, ``"qa-lts"``, ``"prod"`` or
    ``""`` for the main cluster). When omitted, it is discovered from the
    DNS CNAME of ``{location}.clappform.com`` — pass it explicitly in
    air-gapped or split-DNS environments.

    All configuration is explicit constructor input: the library reads no
    config files and no environment variables.
    """

    # Sub-clients are bound dynamically from API_FAMILIES in _bind_services;
    # these annotations give the generated surface (cf.data, cf.client, ...)
    # static types without hand-maintaining the binding.
    if TYPE_CHECKING:
        data: DataAPI
        client: ClientAPI
        auth: AuthAPI
        notifier: NotifierAPI

    def __init__(
        self,
        location: str,
        cluster: str | None = None,
        *,
        api_key: str | None = None,
        credentials: Credentials | None = None,
        endpoints: dict[str, str] | None = None,
        insecure: bool = False,
        timeout: float | None = 60.0,
        retries: RetryPolicy | None = DEFAULT_RETRIES,
        channel_options: list[tuple[str, Any]] | None = None,
        transport: _runtime.Caller | None = None,
    ) -> None:
        if not location:
            raise ConfigurationError("location is required")
        if (api_key is None) == (credentials is None):
            raise ConfigurationError(
                "pass exactly one of api_key= or credentials="
            )
        self._credentials = credentials if credentials is not None else ApiKey(api_key)  # type: ignore[arg-type]
        self.location = location
        self.cluster_discovered = cluster is None
        self.cluster = (
            _discovery.discover_cluster(location) if cluster is None else cluster
        )

        self._init_options: dict[str, Any] = {
            "endpoints": endpoints,
            "insecure": insecure,
            "timeout": timeout,
            "retries": retries,
            "channel_options": channel_options,
        }
        if transport is not None:
            self._transport: _runtime.Caller = transport
            self._owns_transport = False
        else:
            self._transport = GrpcTransport(
                endpoints=resolve_endpoints(self.cluster, endpoints),
                credentials=self._credentials,
                cluster=self.cluster,
                insecure=insecure,
                default_timeout=timeout,
                retries=retries,
                channel_options=channel_options,
            )
            self._owns_transport = True

        self._resolver = _resolve.Resolver(self)
        self._bind_services()

    def _bind_services(self) -> None:
        caller = _BoundCaller(self._transport, self.location)
        for family, api_cls in API_FAMILIES.items():
            setattr(self, family, api_cls(caller))
        self._attach_dataframe_handles()

    def _attach_dataframe_handles(self) -> None:
        """Hang the DataFrame entry points off the generated ``data`` API.

        ``cf.data.collection(ref)`` / ``cf.data.query(ref)`` are the flagship
        surface, but ``data`` is generated ("do not edit"), so they are
        attached here rather than baked into the codegen. Each closes over this
        client so the handle inherits the location and shares the resolver
        cache; the raw generated RPCs on ``cf.data`` are untouched.
        """

        def collection(ref: str) -> dataframes.CollectionHandle:
            return dataframes.CollectionHandle(self, ref)

        def query(ref: str) -> dataframes.QueryHandle:
            return dataframes.QueryHandle(self, ref)

        self.data.collection = collection  # type: ignore[attr-defined]
        self.data.query = query  # type: ignore[attr-defined]

    def with_location(self, location: str) -> Clappform:
        """A clone bound to another tenant, sharing connections when possible.

        With an explicitly configured cluster (or a custom transport) the
        clone inherits it and shares the transport — only the tenant
        metadata differs, and no DNS is performed. When this instance's
        cluster was *discovered*, a different location is re-discovered:
        if it lands on the same cluster the transport is still shared,
        otherwise the clone gets its own transport for its own cluster.
        """
        if not location:
            raise ConfigurationError("location is required")
        if location == self.location:
            return self

        if self.cluster_discovered and self._owns_transport:
            new_cluster = _discovery.discover_cluster(location)
            if new_cluster != self.cluster:
                clone = Clappform(
                    location,
                    new_cluster,
                    credentials=self._credentials,
                    transport=None,
                    **self._init_options,
                )
                clone.cluster_discovered = True
                return clone

        clone = object.__new__(Clappform)
        clone.__dict__.update(self.__dict__)
        clone.location = location
        clone._owns_transport = False  # the parent owns the channels
        clone._bind_services()
        return clone

    def channel_for(self, family: str):
        """The live gRPC channel for an API family (transport-owned only)."""
        if not isinstance(self._transport, GrpcTransport):
            raise ConfigurationError(
                "channel_for() is unavailable with a custom transport"
            )
        return self._transport.channel_for(family)

    def close(self) -> None:
        if self._owns_transport:
            close = getattr(self._transport, "close", None)
            if close is not None:
                close()

    def __enter__(self) -> Clappform:
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.close()

    def __repr__(self) -> str:
        from clappform import __proto_version__, __version__

        cluster = self.cluster or "main"
        discovered = " (discovered)" if self.cluster_discovered else ""
        return (
            f"Clappform(cluster={cluster!r}{discovered}, "
            f"location={self.location!r}, auth={type(self._credentials).__name__}, "
            f"version={__version__}, protos={__proto_version__})"
        )
