"""
This module defines type aliases and a data structure used for configuring gRPC
RPC call options.
"""

from __future__ import annotations

import json
import tempfile
from typing import TYPE_CHECKING

from .proto.clappform.data.v1 import insert_pb2

if TYPE_CHECKING:
    from typing import Iterator, Optional, Union

    import pandas

    from .typedefs import GrpcChannelOptions


def default_options(
    max_attemps: int = 5,
    initial_backoff: str = "0.1s",
    max_backoff: str = "1s",
    backoff_multiplier: int = 2,
    retryable_status_codes: Optional[list[str]] = None,
) -> GrpcChannelOptions:
    """
    Generates default gRPC channel options with retry configuration.

    This function creates a list of gRPC channel options that include retry
    policies and service configuration. It constructs a service
    configuration JSON for gRPC retry policies based on the provided
    parameters.

    :param max_attemps: The maximum number of retry attempts for a failed RPC
                        call. Default is 5.
    :type max_attemps: int
    :param initial_backoff: The initial backoff duration between retry
                            attempts, specified as a string with units
                            (e.g., "0.1s"). Default is "0.1s".
    :type initial_backoff: str
    :param max_backoff: The maximum backoff duration between retry attempts,
                        specified as a string with units (e.g., "1s").
                        Default is "1s".
    :type max_backoff: str
    :param backoff_multiplier: The multiplier applied to the backoff duration
                               for each retry attempt. Default is 2.
    :type backoff_multiplier: int
    :param retryable_status_codes: A list of gRPC status codes that are
                                   considered retryable. If not provided,
                                   defaults to ["UNAVAILABLE"].
    :type retryable_status_codes: Optional[list[str]]

    :return: A list of gRPC channel options as tuples, where each tuple
             consists of an option name and its value.
    :rtype: GrpcChannelOptions

    :example:

    >>> options = default_options()
    >>> print(options)
    [("grpc.enable_retries", 1), ("grpc.service_config", '{"methodConfig": [{"\
name": [{}], "retryPolicy": {"maxAttempts": 5, "initialBackoff": "0.1s", "\
maxBackoff": "1s", "backoffMultiplier": 2, "retryableStatusCodes": ["\
UNAVAILABLE"]}}]}')]

    This function is used to configure gRPC channel options with retry policies
    for better resilience in network operations.
    """
    if retryable_status_codes is None:
        retryable_status_codes = ["UNAVAILABLE"]

    service_config_json = json.dumps(
        {
            "methodConfig": [
                {
                    "name": [{}],
                    "retryPolicy": {
                        "maxAttempts": max_attemps,
                        "initialBackoff": initial_backoff,
                        "maxBackoff": max_backoff,
                        "backoffMultiplier": backoff_multiplier,
                        "retryableStatusCodes": retryable_status_codes,
                    },
                }
            ]
        }
    )
    options: list[tuple[str, Union[int, str]]] = [
        ("grpc.keepalive_time_ms", 120000),
        ("grpc.keepalive_timeout_ms", 20000),
        ("grpc.keepalive_permit_without_calls", True),
        ("grpc.http2.max_pings_without_data", 0),
        ("grpc.http2.min_time_between_pings_ms", 120000),
        ("grpc.http2.min_ping_interval_without_data_ms", 120000),
        ("grpc.enable_retries", 1),
        ("grpc.service_config", service_config_json),
    ]
    return options


def insert_many_dataframe(
    collection: str,
    df: pandas.DataFrame,
    size: int = 2500,
    encoding: str = "utf-8",
) -> Iterator[insert_pb2.InsertRequest]:
    """
    Yields InsertRequest objects for chunks of a DataFrame.

    This function splits a pandas DataFrame into smaller chunks and yields
    `InsertRequest` objects containing JSON-encoded data from each chunk.

    :param collection: The name of the collection where data will be
                       inserted.
    :type collection: str
    :param df: The DataFrame to be split into chunks and inserted.
    :type df: pandas.DataFrame
    :param size: The size of each chunk. Defaults to 2500.
    :type size: int, optional
    :param encoding: The encoding to be used for JSON data.
                     Defaults to "utf-8".
    :type encoding: str, optional
    :return: An iterator over `InsertRequest` objects containing the
             JSON-encoded data.
    :rtype: Iterator[:class:`~clappform.proto.clappform.data.v1.insert_pb2.\
InsertRequest`]

    :raises ValueError: If the DataFrame is empty.
    """
    if df.empty:
        raise ValueError("The DataFrame is empty")

    for chunk in [df[i : i + size] for i in range(0, df.shape[0], size)]:
        # `TemporaryFile` And `force_ascii=False` force the chunck to be
        # `UTF-8` encoded.
        with tempfile.TemporaryFile(mode="w+", encoding=encoding) as fd:
            chunk.to_json(fd, orient="records", force_ascii=False)
            fd.seek(0)  # Reset pointer to begin of file for reading.
            yield insert_pb2.InsertRequest(
                data=fd.read().encode(encoding=encoding),
                collection=collection,
            )
