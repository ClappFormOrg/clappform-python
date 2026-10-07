"""The Clappform client: one instance = one (cluster, location, credentials)
binding.

Nothing is global: two instances pointed at two clusters coexist in one
process, and :meth:`Clappform.with_location` gives a cheap same-cluster
clone for another tenant, sharing connections and configuration.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from clappform import _discovery, _namespace, _resolve, _runtime, dataframes
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

    All configuration is explicit constructor input: the library reads no
    config files and no environment variables.

    Args:
        location: The tenant (environment) subdomain, e.g. ``"acme"`` for
            ``acme.clappform.com``. Sent as ``location`` metadata on every call.
        cluster: The host extension of the cluster serving ``location``:
            ``""`` for the main cluster, or e.g. ``"qa"`` or ``"prod-lts"``.
            ``"prod"`` is accepted as another name for the main cluster
            ``""``; it is *not* ``"prod-lts"``. When omitted, it is discovered
            from the DNS CNAME of ``{location}.clappform.com`` (one lookup,
            at most 5 seconds). Pass it explicitly in air-gapped or split-DNS
            environments. Never discovered when ``transport=`` is given.
        api_key: An API key, sent as ``x-api-key`` metadata. Pass exactly one
            of ``api_key`` and ``credentials``.
        credentials: Any :class:`~clappform.Credentials` implementation, for
            auth flows other than a plain API key.
        endpoints: Per-family address overrides, e.g.
            ``{"data": "localhost:50051"}``. Keys are ``data``, ``client``,
            ``auth`` and ``notifier``; values are used verbatim as
            ``host[:port]``.
        insecure: Use plaintext channels instead of TLS. Local development
            only: the API key then travels unencrypted.
        timeout: Deadline in seconds for unary calls (one request, one
            response) that pass no ``timeout=`` of their own. ``None``
            means no deadline.
        stream_timeout: Deadline in seconds for streaming calls (the DataFrame
            reads and writes, exports, any ``*_stream`` or ``*_many`` RPC)
            that pass no ``timeout=``. Defaults to ``None``: a stream runs
            as long as it keeps moving, and gRPC keepalive detects a dead
            connection. One deadline covers the whole stream, including the
            time your code spends between chunks.
        retries: The :class:`~clappform.RetryPolicy` for ``UNAVAILABLE``
            failures on reads, or ``None`` to disable retries. Writes and
            actions such as ``actionflow.start`` are never retried.
        channel_options: Extra gRPC channel arguments, appended after the
            defaults (keepalive every 30s, 64 MiB message limits).
        transport: A replacement transport, such as
            :class:`~clappform.testing.LocalMock`. The client does not close
            a transport it was given.
    """

    # Sub-clients are bound dynamically from API_FAMILIES in _bind_services;
    # these annotations give the generated surface (cf.data, cf.client, ...)
    # static types without hand-maintaining the binding.
    if TYPE_CHECKING:
        data: DataAPI
        client: ClientAPI
        auth: AuthAPI
        notifier: NotifierAPI

    # Curated top-level conveniences hoisted onto ``cf`` from a deeper path,
    # as an explicit allowlist of ``shortcut -> owning family``. Deliberately
    # tiny: only *globally-unambiguous*, high-traffic entry points belong here,
    # and _attach_dataframe_handles refuses to hoist any name the derived index
    # shows on more than one family. The two-level ``cf.<family>.<service>``
    # path stays the canonical form regardless of what is hoisted.
    #
    # Intentionally empty for now. The obvious DataFrame candidates,
    # ``collection`` / ``query``, are NOT globally unambiguous: both are real
    # service names on cf.client, so hoisting them onto ``cf`` would shadow a
    # different family's surface. They stay at their canonical home,
    # ``cf.data.collection(...)`` / ``cf.data.query(...)``. New entries are
    # added here only after review confirms the name is unambiguous.
    _SHORTCUTS: dict[str, str] = {}

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
        stream_timeout: float | None = None,
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
        # A custom transport owns its own routing, so there is nothing to
        # discover; cluster then stays None unless the caller names one.
        self.cluster_discovered = cluster is None and transport is None
        self.cluster: str | None = (
            _discovery.discover_cluster(location) if self.cluster_discovered else cluster
        )

        self._init_options: dict[str, Any] = {
            "endpoints": endpoints,
            "insecure": insecure,
            "timeout": timeout,
            "stream_timeout": stream_timeout,
            "retries": retries,
            "channel_options": channel_options,
        }
        if transport is not None:
            self._transport: _runtime.Caller = transport
            self._owns_transport = False
        else:
            assert self.cluster is not None  # noqa: S101 -- set or discovered above
            self._transport = GrpcTransport(
                endpoints=resolve_endpoints(self.cluster, endpoints),
                credentials=self._credentials,
                cluster=self.cluster,
                cluster_discovered=self.cluster_discovered,
                insecure=insecure,
                default_timeout=timeout,
                stream_timeout=stream_timeout,
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

        for name, handle in (("collection", collection), ("query", query)):
            if hasattr(self.data, name):
                # A generated cf.data service with this name would be shadowed.
                raise ConfigurationError(
                    f"cf.data.{name} is generated and would be shadowed by the "
                    f"DataFrame handle; rename one of them"
                )
            setattr(self.data, name, handle)

        # Hoist the curated shortcuts onto the client itself so cf.collection(...)
        # resolves to the same callable as cf.data.collection(...). The
        # allowlist is checked against the derived name index so an ambiguous
        # name can never be hoisted silently.
        index = _namespace.name_index()
        for shortcut, family in self._SHORTCUTS.items():
            owners = index.get(shortcut)
            if owners is not None and owners != [family]:
                raise ConfigurationError(
                    f"refusing to hoist ambiguous shortcut {shortcut!r}: "
                    f"it also names a service/method on {owners}"
                )
            target = getattr(self, family)
            if not hasattr(target, shortcut):
                raise ConfigurationError(
                    f"cannot hoist shortcut {shortcut!r}: "
                    f"cf.{family} has no attribute {shortcut!r}"
                )
            setattr(self, shortcut, getattr(target, shortcut))

    def with_location(self, location: str) -> Clappform:
        """A clone bound to another tenant, sharing connections when possible.

        With an explicitly configured cluster (or a custom transport) the
        clone inherits it and shares the transport; only the tenant
        metadata differs, and no DNS is performed. When this instance's
        cluster was *discovered*, a different location is re-discovered:
        if it lands on the same cluster the transport is still shared,
        otherwise the clone gets its own transport for its own cluster.

        Lifecycle: a clone that shares the transport stops working once this
        client is closed, and closing the clone does nothing. A clone with
        its own transport must be closed itself; use it as a context
        manager (``with cf.with_location("other") as other: ...``); that is
        safe for a shared clone too, including one for this same location.
        """
        if not location:
            raise ConfigurationError("location is required")

        # Clones of clones re-discover as well: a shared clone keeps the
        # discovered flag, so it can still route a location on another cluster.
        if self.cluster_discovered and location != self.location:
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
                # Errors from the clone's own transport mark the cluster as
                # discovered, the same as the parent's do.
                clone._transport.cluster_discovered = True  # type: ignore[attr-defined]
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

    def __getattr__(self, name: str) -> Any:
        """Turn a wrong-family / typo access into an actionable error.

        Only reached when normal lookup misses (the bound families and curated
        shortcuts resolve first). If ``name`` is a real service or method name
        living on a family, say so: ``cf.insert`` -> "``insert`` lives on
        cf.data". Otherwise fall back to the standard ``AttributeError``.
        """
        # Dunder / private probes (copy, pickle, etc.) must miss cleanly.
        if name.startswith("_"):
            raise AttributeError(name)
        hint = _namespace.wrong_family_hint(name)
        if hint is not None:
            raise AttributeError(hint)
        raise AttributeError(f"{type(self).__name__!r} object has no attribute {name!r}")

    def __dir__(self) -> list[str]:
        """List the four families and the curated shortcuts alongside the
        regular attributes, so tab-completion surfaces the entry points."""
        from clappform.services import API_FAMILIES

        names = set(super().__dir__())
        names.update(API_FAMILIES)
        names.update(self._SHORTCUTS)
        return sorted(names)

    def help(self, name: str | None = None) -> str:
        """Answer "which family owns ``<name>``?", or list the families.

        With no argument, returns the four family names plus curated shortcuts.
        With a name, returns the wrong-family hint (or notes it is unknown).
        """
        from clappform.services import API_FAMILIES

        if name is None:
            families = ", ".join(f"cf.{f}" for f in sorted(API_FAMILIES))
            summary = f"API families: {families}."
            if self._SHORTCUTS:
                shortcuts = ", ".join(f"cf.{s}" for s in sorted(self._SHORTCUTS))
                summary += f" Shortcuts: {shortcuts}."
            return summary
        hint = _namespace.wrong_family_hint(name)
        if hint is not None:
            return hint
        return f"{name!r} is not a known Clappform service or method"

    def __repr__(self) -> str:
        from clappform import __proto_version__, __version__

        cluster = "custom transport" if self.cluster is None else repr(self.cluster or "main")
        discovered = " (discovered)" if self.cluster_discovered else ""
        return (
            f"Clappform(cluster={cluster}{discovered}, "
            f"location={self.location!r}, auth={type(self._credentials).__name__}, "
            f"version={__version__}, protos={__proto_version__})"
        )
