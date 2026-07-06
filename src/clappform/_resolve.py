"""Slug/name -> UUID resolution for collections and saved queries.

The data plane identifies collections and saved queries by UUID, but both
entities also carry a human identifier — a ``slug`` for collections, a
``name`` for saved queries — and that is what people remember. So the
DataFrame entry points accept either: a string that already parses as a UUID
is used as-is with zero overhead, and anything else is treated as a human
identifier and resolved through the Client API on first use.

Resolutions are cached per location on the owning client, so a slug costs one
extra lookup per process, not per call. A cached UUID that later comes back
``NOT_FOUND`` (the entity was recreated, or its slug remapped) is re-resolved
once before the error is surfaced. An identifier that matches nothing raises
:class:`NotFoundError`, naming both the identifier and the location searched.
"""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from clappform._errors import NotFoundError

if TYPE_CHECKING:
    from clappform._client import Clappform


def is_uuid(ref: str) -> bool:
    """Whether ``ref`` is a UUID string (any standard form) usable as-is.

    Accepts the canonical hyphenated form and the other layouts
    :class:`uuid.UUID` parses (braces, urn, bare hex); rejects everything
    else, which is then treated as a slug/name to resolve.
    """
    try:
        uuid.UUID(ref)
    except (ValueError, AttributeError):
        return False
    return True


class Resolver:
    """Per-client slug/name -> UUID resolver, cached per location.

    One instance is held by a :class:`~clappform._client.Clappform`; its
    ``with_location`` clones share it, and the cache is keyed by location so a
    slug resolved for one tenant is never reused for another.
    """

    __slots__ = ("_client", "_collections", "_queries")

    def __init__(self, client: Clappform) -> None:
        self._client = client
        # location -> {slug/name: uuid}
        self._collections: dict[str, dict[str, str]] = {}
        self._queries: dict[str, dict[str, str]] = {}

    def collection_id(self, ref: str, location: str) -> str:
        """The UUID for a collection ``ref`` (slug or UUID) at ``location``."""
        if is_uuid(ref):
            return ref
        return self._cached(self._collections, ref, location, self._lookup_collection)

    def query_id(self, ref: str, location: str) -> str:
        """The UUID for a saved query ``ref`` (name or UUID) at ``location``."""
        if is_uuid(ref):
            return ref
        return self._cached(self._queries, ref, location, self._lookup_query)

    def invalidate_collection(self, ref: str, location: str) -> None:
        """Drop any cached collection UUID for ``ref`` at ``location``.

        Called when a cached UUID comes back ``NOT_FOUND`` so the next use
        re-resolves the slug rather than reusing a stale mapping.
        """
        self._collections.get(location, {}).pop(ref, None)

    def invalidate_query(self, ref: str, location: str) -> None:
        """Drop any cached saved-query UUID for ``ref`` at ``location``."""
        self._queries.get(location, {}).pop(ref, None)

    # -- internals -------------------------------------------------------

    def _cached(self, cache, ref, location, lookup):
        by_ref = cache.setdefault(location, {})
        cached = by_ref.get(ref)
        if cached is not None:
            return cached
        resolved = lookup(ref, location)
        by_ref[ref] = resolved
        return resolved

    def _lookup_collection(self, slug: str, location: str) -> str:
        for collection in self._client.client.collection.iter_get_all(location=location):
            if collection.slug == slug:
                return collection.id
        raise NotFoundError(
            f"no collection with slug {slug!r} found",
            location=location,
            cluster=self._client.cluster,
        )

    def _lookup_query(self, name: str, location: str) -> str:
        for query in self._client.client.query.iter_get_all(location=location):
            if query.name == name:
                return query.id
        raise NotFoundError(
            f"no saved query named {name!r} found",
            location=location,
            cluster=self._client.cluster,
        )
