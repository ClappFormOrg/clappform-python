"""Typed exception hierarchy for the Clappform client.

Users never need to import ``grpc`` to handle a failure: every error the
client raises derives from :class:`ClappformError`, and each one carries the
call context (API family, method, cluster, location) so "which tenant on
which cluster failed" is always in the message.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import grpc


class ClappformError(Exception):
    """Base class for every error raised by the Clappform client."""

    def __init__(
        self,
        message: str,
        *,
        status: str | None = None,
        method: str | None = None,
        cluster: str | None = None,
        cluster_discovered: bool = False,
        location: str | None = None,
        details: str | None = None,
    ) -> None:
        self.status = status
        self.method = method
        self.cluster = cluster
        self.cluster_discovered = cluster_discovered
        self.location = location
        self.details = details
        context = []
        if method:
            context.append(f"method={method}")
        if cluster is not None:
            # Mark a DNS-discovered cluster so a wrong discovery is visible in
            # the failure itself, not just in repr(client).
            discovered = " (discovered)" if cluster_discovered else ""
            context.append(f"cluster={(cluster or 'main')!r}{discovered}")
        if location:
            context.append(f"location={location!r}")
        if status:
            context.append(f"status={status}")
        suffix = f" ({', '.join(context)})" if context else ""
        super().__init__(f"{message}{suffix}")


class ConfigurationError(ClappformError):
    """Bad endpoints, credentials, or cluster settings — raised before any
    RPC is attempted, or when the server reports missing call configuration."""


class AuthenticationError(ClappformError):
    """The server rejected the call's credentials (UNAUTHENTICATED)."""


class PermissionDeniedError(ClappformError):
    """Authenticated, but not allowed to perform this call (PERMISSION_DENIED)."""


class NotFoundError(ClappformError):
    """The referenced entity does not exist (NOT_FOUND)."""


class InvalidRequestError(ClappformError):
    """The request was malformed or violated a precondition
    (INVALID_ARGUMENT / FAILED_PRECONDITION / OUT_OF_RANGE)."""


class ConflictError(ClappformError):
    """The call conflicts with existing state (ALREADY_EXISTS / ABORTED)."""


class NotSupportedError(ClappformError):
    """The server does not implement this RPC (UNIMPLEMENTED). Clusters are
    updated at different times, so a newer client may call an RPC an older
    cluster does not serve yet."""


class TransientError(ClappformError):
    """The call failed in a retryable way and retries were exhausted
    (UNAVAILABLE / DEADLINE_EXCEEDED)."""


# The authoriser's location interceptor aborts calls that carry no usable
# tenant header with this message; surface it as a configuration problem.
_LOCATION_HEADER_DETAIL = "invalid/missing header: 'location'"

_STATUS_MAP: dict[str, type[ClappformError]] = {
    "UNAUTHENTICATED": AuthenticationError,
    "PERMISSION_DENIED": PermissionDeniedError,
    "NOT_FOUND": NotFoundError,
    "INVALID_ARGUMENT": InvalidRequestError,
    "FAILED_PRECONDITION": InvalidRequestError,
    "OUT_OF_RANGE": InvalidRequestError,
    "ALREADY_EXISTS": ConflictError,
    "ABORTED": ConflictError,
    "UNIMPLEMENTED": NotSupportedError,
    "UNAVAILABLE": TransientError,
    "DEADLINE_EXCEEDED": TransientError,
}


def translate_rpc_error(
    error: grpc.RpcError,
    *,
    method: str | None = None,
    cluster: str | None = None,
    cluster_discovered: bool = False,
    location: str | None = None,
) -> ClappformError:
    """Map a grpc.RpcError onto the typed hierarchy, preserving call context."""
    status = getattr(error, "code", lambda: None)()
    status_name = status.name if status is not None else "UNKNOWN"
    details = getattr(error, "details", lambda: "")() or ""

    if _LOCATION_HEADER_DETAIL in details:
        return ConfigurationError(
            f"{details} — the server received no usable tenant header; "
            f"check the location= argument",
            status=status_name,
            method=method,
            cluster=cluster,
            cluster_discovered=cluster_discovered,
            location=location,
            details=details,
        )

    exc_cls = _STATUS_MAP.get(status_name, ClappformError)
    message = details or f"RPC failed with status {status_name}"
    if exc_cls is NotSupportedError:
        message = (
            f"{message} — this cluster may not serve this RPC yet; "
            f"cluster rollouts are staggered"
        )
    return exc_cls(
        message,
        status=status_name,
        method=method,
        cluster=cluster,
        cluster_discovered=cluster_discovered,
        location=location,
        details=details,
    )
