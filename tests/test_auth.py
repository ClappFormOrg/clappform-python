"""API-key credential behaviour."""

import pytest

from clappform._auth import ApiKey, Credentials
from clappform._errors import ConfigurationError


def test_api_key_emits_x_api_key_metadata() -> None:
    assert ApiKey("secret").metadata_for_call() == (("x-api-key", "secret"),)


def test_api_key_satisfies_credentials_protocol() -> None:
    assert isinstance(ApiKey("secret"), Credentials)


@pytest.mark.parametrize("bad", ["", "   "])
def test_blank_api_key_rejected(bad: str) -> None:
    with pytest.raises(ConfigurationError, match="non-empty"):
        ApiKey(bad)


def test_repr_never_leaks_the_key() -> None:
    assert "secret" not in repr(ApiKey("secret"))
