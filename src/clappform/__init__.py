"""Python client for the Clappform gRPC APIs."""

from clappform import _runtime  # noqa: F401  (must precede _client: services import it)
from clappform._auth import ApiKey, Credentials
from clappform._client import Clappform
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
)
from clappform._proto_version import __proto_version__
from clappform._transport import DEFAULT_RETRIES, RetryPolicy
from clappform.dataframes import CollectionHandle, QueryHandle, ReadResult

# The one place the release version lives; hatchling reads this literal for the
# packaged version (see [tool.hatch.version] in pyproject.toml).
__version__ = "6.0.0a1"

__all__ = [
    "DEFAULT_RETRIES",
    "ApiKey",
    "AuthenticationError",
    "Clappform",
    "ClappformError",
    "CollectionHandle",
    "ConfigurationError",
    "ConflictError",
    "Credentials",
    "InvalidRequestError",
    "QueryHandle",
    "ReadResult",
    "NotFoundError",
    "NotSupportedError",
    "PermissionDeniedError",
    "RetryPolicy",
    "TransientError",
    "__proto_version__",
    "__version__",
]
