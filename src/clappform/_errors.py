"""Typed exception hierarchy for the Clappform client.

Users should never need to import ``grpc`` to handle a failure: everything
the client raises derives from :class:`ClappformError`. The hierarchy grows
alongside the transport layer; only the configuration-time errors live here
so far.
"""

from __future__ import annotations


class ClappformError(Exception):
    """Base class for every error raised by the Clappform client."""


class ConfigurationError(ClappformError):
    """Bad endpoints, credentials, or cluster settings — raised before any
    RPC is attempted."""
