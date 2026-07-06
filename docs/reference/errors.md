# Errors

Every error the client raises derives from `ClappformError` and carries the
call context (method, cluster, location). See
[Error handling & retries](../guides/errors-and-retries.md) for how the gRPC
status codes map onto these types.

::: clappform.ClappformError

::: clappform.ConfigurationError

::: clappform.AuthenticationError

::: clappform.PermissionDeniedError

::: clappform.NotFoundError

::: clappform.InvalidRequestError

::: clappform.ConflictError

::: clappform.NotSupportedError

::: clappform.TransientError
