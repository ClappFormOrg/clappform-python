"""Name -> API-family index for friendly wrong-family / typo errors.

The public surface is intentionally two levels deep (``cf.data.insert(...)``,
``cf.auth.api_key(...)``) because names are only unique at the gRPC-path level,
not at the flat Python-attribute level (``create`` / ``get`` / ``delete`` recur
across ~22 services, and ``general`` / ``process`` / ``version`` name services in
more than one family, on different hosts). Flattening the surface onto ``cf``
would silently misroute; see DESIGN.md §3.2.

So the family segment stays, and this module delivers the ergonomics the
flattening was reaching for: reach for a service or method name on the wrong
object and you get told its real home instead of a bare ``AttributeError``.

The index is *derived* from :data:`clappform.services.API_FAMILIES` at import
time, never hand-maintained: a new RPC in the generated layer appears in the
hint automatically. Colliding names map to *all* their owning families rather
than guessing one.
"""

from __future__ import annotations

from functools import lru_cache


class _NullCaller:
    """A do-nothing caller used only to instantiate family classes for
    introspection. Family/service constructors just stash the caller, so no RPC
    is ever attempted through this."""

    def invoke(self, *args: object, **kwargs: object) -> object:  # pragma: no cover - never called
        raise RuntimeError("introspection caller must not be invoked")


def _iter_service_and_method_names(family_cls: type) -> tuple[list[str], dict[str, list[str]]]:
    """Return (service attribute names, {method_name: [service names]}) for a
    family class, by introspecting a throwaway instance."""
    instance = family_cls(_NullCaller())
    services: list[str] = []
    methods: dict[str, list[str]] = {}
    for attr in vars(instance):
        if attr.startswith("_"):
            continue
        services.append(attr)
        service = getattr(instance, attr)
        for name in dir(type(service)):
            if name.startswith("_"):
                continue
            if callable(getattr(type(service), name, None)):
                methods.setdefault(name, []).append(attr)
    return services, methods


@lru_cache(maxsize=1)
def name_index() -> dict[str, list[str]]:
    """Map every service and method name to the families that own it.

    Built once and cached. A name owned by several families (e.g. ``general``,
    ``process``) lists all of them, sorted, so the hint can name every home
    rather than picking one.
    """
    from clappform.services import API_FAMILIES

    index: dict[str, set[str]] = {}
    for family, family_cls in API_FAMILIES.items():
        services, methods = _iter_service_and_method_names(family_cls)
        for service_name in services:
            index.setdefault(service_name, set()).add(family)
        for method_name in methods:
            index.setdefault(method_name, set()).add(family)
    return {name: sorted(families) for name, families in index.items()}


def wrong_family_hint(name: str) -> str | None:
    """A one-line hint telling the caller where ``name`` actually lives, or
    ``None`` if the name is not a known service/method anywhere.

    Colliding names name every owning family so the caller is never quietly
    pointed at the wrong host.
    """
    families = name_index().get(name)
    if not families:
        return None
    if len(families) == 1:
        family = families[0]
        return f"{name!r} lives on cf.{family}, not on the client directly"
    homes = " or ".join(f"cf.{f}" for f in families)
    return (
        f"{name!r} exists on more than one API family ({homes}); "
        f"reach it through the family that owns your data"
    )
