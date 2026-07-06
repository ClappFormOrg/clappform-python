# Error handling & retries

Every failure the client raises derives from
[`ClappformError`][clappform.ClappformError] and carries the call context —
method, cluster, location — so you never import `grpc` to handle one, and the
message always says which tenant on which cluster failed.

## The typed hierarchy

gRPC status codes are mapped onto specific exception types:

| Exception | gRPC status | Meaning |
|---|---|---|
| [`ConfigurationError`][clappform.ConfigurationError] | (pre-flight / missing header) | Bad endpoints, credentials, or a missing tenant header — often raised before any RPC |
| [`AuthenticationError`][clappform.AuthenticationError] | `UNAUTHENTICATED` | The credential was rejected |
| [`PermissionDeniedError`][clappform.PermissionDeniedError] | `PERMISSION_DENIED` | Authenticated, but not allowed |
| [`NotFoundError`][clappform.NotFoundError] | `NOT_FOUND` | The referenced entity does not exist |
| [`InvalidRequestError`][clappform.InvalidRequestError] | `INVALID_ARGUMENT` / `FAILED_PRECONDITION` / `OUT_OF_RANGE` | Malformed request or violated precondition |
| [`ConflictError`][clappform.ConflictError] | `ALREADY_EXISTS` / `ABORTED` | Conflicts with existing state |
| [`NotSupportedError`][clappform.NotSupportedError] | `UNIMPLEMENTED` | This cluster doesn't serve the RPC yet (staggered rollouts) |
| [`TransientError`][clappform.TransientError] | `UNAVAILABLE` / `DEADLINE_EXCEEDED` | Retryable failure, retries exhausted |

## Catching errors

Catch the specific type you can act on and let the rest propagate:

```python
--8<-- "errors_and_retries.py:typed-errors"
```

## Retries

Retries are configured once on the client and applied by gRPC's built-in retry
support. The default, `clappform.DEFAULT_RETRIES`, retries `UNAVAILABLE` with
exponential backoff. Override it per client with a
[`RetryPolicy`][clappform.RetryPolicy], or pass `retries=None` to disable.

```python
--8<-- "errors_and_retries.py:retry-policy"
```

!!! warning "Retries and streaming writes"
    Chunked uploads (`append`, `update`, `upsert`) stream in chunks, so a failed
    chunk is retryable at the flow level. When a `TransientError` escapes after
    retries are exhausted, retry the whole flow rather than a single chunk — the
    write is designed to be safe to re-run.

See the [Errors reference](../reference/errors.md) for the full hierarchy.
