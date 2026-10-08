"""Credentials for the Clappform APIs.

v1 ships API keys only. The :class:`Credentials` protocol is the seam other
flows (token exchange, SSO) plug into later: a credential's only job is to
contribute metadata to each call.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, runtime_checkable

from clappform._errors import ConfigurationError


@runtime_checkable
class Credentials(Protocol):
    """Anything that can attach auth metadata to a call."""

    def metadata_for_call(self) -> tuple[tuple[str, str], ...]: ...


@dataclass(frozen=True)
class ApiKey:
    """API-key credential, sent as ``x-api-key`` metadata on every call."""

    key: str

    def __post_init__(self) -> None:
        if not self.key or not self.key.strip():
            raise ConfigurationError("api_key must be a non-empty string")

    def metadata_for_call(self) -> tuple[tuple[str, str], ...]:
        return (("x-api-key", self.key),)

    def __repr__(self) -> str:  # never leak the key into logs or errors
        return "ApiKey(***)"
