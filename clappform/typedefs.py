"""
This module defines type aliases and data structures used for gRPC RPC call
options.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional, Sequence, TypeAlias, TypedDict, Union

    import grpc

GrpcChannelOptions: TypeAlias = Sequence[tuple[str, Union[int, str]]]
"""
GrpcChannelOptions is a type alias representing a sequence of gRPC
channel options.

Each option is a tuple consisting of a string option name and its value,
which can be either an integer or a string.

Example:
    options = [
        ("grpc.enable_retries", 1),
        ("grpc.service_config", '{"methodConfig": [...]}')
    ]

This type alias is used to configure various gRPC channel settings to
customize the behavior of the gRPC client.

Usage:
    .. code-block:: python

        from clappform.typedefs import GrpcChannelOptions

        options: GrpcChannelOptions = [
            ("grpc.enable_retries", 1),
            ("grpc.service_config", '{"methodConfig": [...]}')
        ]

        # Use options in gRPC channel creation
        channel = grpc.insecure_channel('localhost:50051', options)
"""

GrpcMetadata: TypeAlias = tuple[tuple[str, str | bytes], ...]
"""
GrpcMetadata is a type alias representing a tuple of metadata for gRPC
calls.

Each metadata entry is a tuple consisting of a string key and a value,
which can be either a string or bytes.

Example:
    metadata = (("x-api-key", "data"), ("location", b"data"))

This type alias is used to send additional metadata with gRPC calls,
such as authentication tokens or other contextual information.

Usage:
    .. code-block:: python

        from clappform.typedefs import GrpcMetadata

        metadata: GrpcMetadata = (
            ("x-api-key", "data"),
            ("location", b"data")
        )

        # Use metadata in gRPC call
        response = stub.MyMethod(request, metadata=metadata)
"""


class RpcCallOptions(TypedDict, total=False):
    """
    RpcCallOptions is a TypedDict for specifying options for an RPC call.

    :param timeout: The timeout for the RPC call in seconds. If None, no
                    timeout is set.
    :type timeout: Optional[float]
    :param metadata: The metadata to send with the RPC call.
                     If None, no additional metadata is sent.
    :type metadata: Optional[:py:data:`~clappform.typedefs.GrpcMetadata`]
    :param credentials: Call credentials for the RPC call.
                        If None, no additional credentials are used.
    :type credentials: Optional[grpc.CallCredentials]
    :param wait_for_ready: Whether the RPC should wait for the channel to
                           be ready. If None, the default behavior is used.
    :type wait_for_ready: Optional[bool]
    :param compression: The compression algorithm to use for the RPC call.
                        If None, no compression is used.
    :type compression: Optional[
                           grpc.Compression
                       ]

    This TypedDict allows for flexible and detailed configuration of gRPC
    calls, enabling customization of timeout, metadata, credentials,
    readiness, and compression settings.

    Usage:
        .. code-block:: python

            from clappform.typedefs import RpcCallOptions

            options: RpcCallOptions = {
                "timeout": 10.0,
                "metadata": (("x-api-key", "data"),),
                "credentials": my_credentials,
                "wait_for_ready": True,
                "compression": grpc.Compression.Gzip
            }

            # Use options in gRPC call
            response = stub.MyMethod(request, **options)
    """

    timeout: Optional[float]
    metadata: Optional[GrpcMetadata]
    credentials: Optional[grpc.CallCredentials]
    wait_for_ready: Optional[bool]
    compression: Optional[grpc.Compression]
