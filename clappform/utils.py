"""
This module defines type aliases and a data structure used for configuring gRPC RPC call options.
"""

import json
from typing import Optional, Union

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
    [("grpc.enable_retries", 1), ("grpc.service_config", '{"methodConfig": [{"name": [{}], "retryPolicy": {"maxAttempts": 5, "initialBackoff": "0.1s", "maxBackoff": "1s", "backoffMultiplier": 2, "retryableStatusCodes": ["UNAVAILABLE"]}}]}')]

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
    options: list[tuple[str, Union[int, str]]] = []
    options.append(("grpc.enable_retries", 1))
    options.append(("grpc.service_config", service_config_json))
    return options
