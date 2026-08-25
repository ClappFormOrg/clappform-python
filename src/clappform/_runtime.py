"""Runtime support for the generated service layer.

Generated service classes never import ``grpc`` directly: every RPC goes
through a :class:`Caller`, which owns channels, credentials, metadata,
deadlines, and retries. The real gRPC transport and any test double both
implement this one protocol, so the generated code works identically against
either.
"""

from __future__ import annotations

from collections.abc import Iterable, Iterator
from typing import Any, Literal, Protocol, TypeVar

ResponseT = TypeVar("ResponseT")

CallKind = Literal["unary_unary", "unary_stream", "stream_unary", "stream_stream"]


class Caller(Protocol):
    """Transport seam used by all generated service methods.

    ``method`` is the full gRPC method path, e.g.
    ``/clappform.data.v1.insert.InsertManagement/InsertSingle``.
    ``request`` is a request message for unary-input calls or an iterable of
    request messages for stream-input calls. Implementations return the
    response message for unary-output calls or an iterator of response
    messages for stream-output calls.
    """

    def invoke(
        self,
        kind: CallKind,
        method: str,
        request: Any,
        request_cls: type,
        response_cls: type,
        *,
        timeout: float | None = None,
        metadata: tuple[tuple[str, str], ...] | None = None,
        location: str | None = None,
    ) -> Any: ...


class ServiceBase:
    """Base class for generated per-service wrappers."""

    __slots__ = ("_caller",)

    def __init__(self, caller: Caller) -> None:
        self._caller = caller


def build_request(request_cls: type, request: Any, kwargs: dict[str, Any]) -> Any:
    """Resolve the message-or-kwargs calling convention of generated methods.

    Callers pass either a prebuilt request message or flattened field
    keyword arguments, never both. ``kwargs`` holds only the fields the
    caller actually provided (``None`` values are dropped by the generated
    method before calling this).
    """
    if request is not None:
        if kwargs:
            provided = ", ".join(sorted(kwargs))
            raise TypeError(
                f"pass either a {request_cls.__name__} message or field keyword "
                f"arguments, not both (got message plus: {provided})"
            )
        if not isinstance(request, request_cls):
            raise TypeError(
                f"request must be {request_cls.__name__}, got {type(request).__name__}"
            )
        return request
    return request_cls(**kwargs)


def ensure_iterable(requests: Iterable[Any], request_cls: type) -> Iterator[Any]:
    """Validate a stream-input argument lazily, yielding each request."""
    for item in requests:
        if not isinstance(item, request_cls):
            raise TypeError(
                f"stream items must be {request_cls.__name__}, got {type(item).__name__}"
            )
        yield item
