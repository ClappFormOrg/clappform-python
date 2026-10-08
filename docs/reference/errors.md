# Errors

A failed call raises a subclass of `ClappformError` carrying the call context
(method, cluster, location). Argument mistakes caught before a call raise
`ValueError`, `TypeError`, `NotImplementedError` or `AttributeError` instead;
[Errors raised before a call](../guides/errors-and-retries.md#errors-raised-before-a-call)
lists when. See [Error handling & retries](../guides/errors-and-retries.md) for
how the gRPC status codes map onto these types.

::: clappform.ClappformError

::: clappform.ConfigurationError

::: clappform.AuthenticationError

::: clappform.PermissionDeniedError

::: clappform.NotFoundError

::: clappform.InvalidRequestError

::: clappform.ConflictError

::: clappform.ResourceExhaustedError

::: clappform.NotSupportedError

::: clappform.TransientError
