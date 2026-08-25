"""DNS-based cluster discovery.

Every client environment (``location``) is a CNAME to its cluster's BigIP,
and the BigIP hostname carries the same extension as that cluster's service
hosts::

    gelderland.clappform.com     CNAME  bigip.clappform.com           -> cluster ""
    noord-brabant.clappform.com  CNAME  bigip-prod-lts.clappform.com  -> cluster "prod-lts"

So one forward lookup of ``{location}.clappform.com`` yields the cluster
extension: no reverse lookups, no registry, no extra dependencies. This
module only derives the extension; which endpoints to build from it, and
per-instance caching, belong to the client constructor. The ``location``
metadata header sent on every call is unaffected.

Discovery never guesses: any lookup failure or unexpected canonical name
raises :class:`~clappform._errors.ConfigurationError` telling the caller to
pass ``cluster=`` explicitly. Notably, resolvers that do not report
canonical names (musl-based systems such as Alpine containers echo the
queried name back) land in that error path instead of misresolving.
"""

from __future__ import annotations

import re
import socket
from collections.abc import Callable

from clappform._errors import ConfigurationError

BASE_DOMAIN = "clappform.com"

# Canonical name of a cluster's BigIP: bigip.clappform.com for the main
# cluster, bigip-<extension>.clappform.com for every other one. A trailing
# dot (FQDN form) is tolerated.
_CANONICAL = re.compile(
    r"^bigip(?:-(?P<ext>[a-z0-9-]+))?\.clappform\.com\.?$",
    re.IGNORECASE,
)

# Returns the canonical hostname for the given hostname (CNAME chain target).
Resolver = Callable[[str], str]


def _default_resolver(host: str) -> str:
    return socket.gethostbyname_ex(host)[0]


def discover_cluster(location: str, *, resolver: Resolver | None = None) -> str:
    """Derive the cluster extension for *location* from its CNAME target.

    Returns the extension string: ``""`` for the main cluster,
    ``"prod-lts"``-style values for every other cluster.

    Raises :class:`ConfigurationError` when the lookup fails or the
    canonical name does not match the BigIP convention. Pass ``cluster=``
    explicitly in that case.
    """
    if not location or not re.fullmatch(r"[a-z0-9-]+", location, re.IGNORECASE):
        raise ConfigurationError(
            f"cannot discover a cluster for location {location!r}: not a valid "
            f"subdomain label; pass cluster= explicitly"
        )
    host = f"{location}.{BASE_DOMAIN}"
    resolve = resolver or _default_resolver
    try:
        canonical = resolve(host)
    except OSError as exc:  # socket.gaierror and friends
        raise ConfigurationError(
            f"cluster discovery failed: could not resolve {host!r} ({exc}); "
            f"pass cluster= explicitly"
        ) from exc

    match = _CANONICAL.match(canonical)
    if match is None:
        raise ConfigurationError(
            f"cluster discovery failed: {host!r} resolved to canonical name "
            f"{canonical!r}, which does not match the expected "
            f"bigip[-<cluster>].{BASE_DOMAIN} convention; pass cluster= explicitly"
        )
    return (match.group("ext") or "").lower()
