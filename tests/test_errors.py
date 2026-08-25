"""gRPC status translation into the typed error hierarchy."""

import grpc
import pytest

from clappform._errors import (
    AuthenticationError,
    ClappformError,
    ConfigurationError,
    ConflictError,
    InvalidRequestError,
    NotFoundError,
    NotSupportedError,
    PermissionDeniedError,
    TransientError,
    translate_rpc_error,
)


class FakeRpcError(grpc.RpcError):
    def __init__(self, code: grpc.StatusCode, details: str = "") -> None:
        self._code = code
        self._details = details

    def code(self) -> grpc.StatusCode:
        return self._code

    def details(self) -> str:
        return self._details


@pytest.mark.parametrize(
    ("status", "expected"),
    [
        (grpc.StatusCode.UNAUTHENTICATED, AuthenticationError),
        (grpc.StatusCode.PERMISSION_DENIED, PermissionDeniedError),
        (grpc.StatusCode.NOT_FOUND, NotFoundError),
        (grpc.StatusCode.INVALID_ARGUMENT, InvalidRequestError),
        (grpc.StatusCode.FAILED_PRECONDITION, InvalidRequestError),
        (grpc.StatusCode.ALREADY_EXISTS, ConflictError),
        (grpc.StatusCode.ABORTED, ConflictError),
        (grpc.StatusCode.UNIMPLEMENTED, NotSupportedError),
        (grpc.StatusCode.UNAVAILABLE, TransientError),
        (grpc.StatusCode.DEADLINE_EXCEEDED, TransientError),
        (grpc.StatusCode.INTERNAL, ClappformError),
    ],
)
def test_status_maps_to_typed_error(status, expected) -> None:
    error = translate_rpc_error(FakeRpcError(status, "boom"))
    assert type(error) is expected
    assert error.status == status.name


def test_context_appears_in_message() -> None:
    error = translate_rpc_error(
        FakeRpcError(grpc.StatusCode.NOT_FOUND, "no such collection"),
        method="/clappform.data.v1.x.Y/Get",
        cluster="qa-lts",
        location="acme",
    )
    text = str(error)
    assert "no such collection" in text
    assert "cluster='qa-lts'" in text
    assert "location='acme'" in text
    assert "status=NOT_FOUND" in text


def test_empty_cluster_reads_as_main() -> None:
    error = translate_rpc_error(
        FakeRpcError(grpc.StatusCode.NOT_FOUND, "x"), cluster="", location="acme"
    )
    assert "cluster='main'" in str(error)


def test_discovered_cluster_is_flagged_in_the_error() -> None:
    # A DNS-discovered cluster is marked so a wrong discovery is visible in the
    # failure itself, not only in repr(client).
    error = translate_rpc_error(
        FakeRpcError(grpc.StatusCode.NOT_FOUND, "x"),
        cluster="prod-lts",
        cluster_discovered=True,
        location="acme",
    )
    assert "cluster='prod-lts' (discovered)" in str(error)
    assert error.cluster_discovered is True


def test_explicit_cluster_is_not_flagged_as_discovered() -> None:
    error = translate_rpc_error(
        FakeRpcError(grpc.StatusCode.NOT_FOUND, "x"),
        cluster="prod-lts",
        cluster_discovered=False,
        location="acme",
    )
    assert "(discovered)" not in str(error)
    assert error.cluster_discovered is False


def test_discovered_main_cluster_reads_as_main_discovered() -> None:
    error = translate_rpc_error(
        FakeRpcError(grpc.StatusCode.NOT_FOUND, "x"),
        cluster="",
        cluster_discovered=True,
        location="acme",
    )
    assert "cluster='main' (discovered)" in str(error)


def test_missing_location_header_becomes_configuration_error() -> None:
    error = translate_rpc_error(
        FakeRpcError(grpc.StatusCode.ABORTED, "invalid/missing header: 'location'"),
        location=None,
    )
    assert isinstance(error, ConfigurationError)
    assert "location=" in str(error)


def test_unimplemented_carries_staggered_rollout_hint() -> None:
    error = translate_rpc_error(FakeRpcError(grpc.StatusCode.UNIMPLEMENTED, "nope"))
    assert "may not serve this RPC yet" in str(error)


def test_everything_catchable_via_base() -> None:
    error = translate_rpc_error(FakeRpcError(grpc.StatusCode.UNKNOWN, ""))
    assert isinstance(error, ClappformError)
