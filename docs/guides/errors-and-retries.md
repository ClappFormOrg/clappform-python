# Error handling & retries

A call that fails raises a subclass of
[`ClappformError`][clappform.ClappformError] carrying the call context
(method, cluster, location), so you never import `grpc` to handle one, and the
message says which tenant on which cluster failed. Mistakes in the arguments
you pass are caught before any call and raise the standard Python exceptions
listed under [Errors raised before a call](#errors-raised-before-a-call).

## The typed hierarchy

gRPC status codes are mapped onto specific exception types:

| Exception | gRPC status | Meaning |
|---|---|---|
| [`ConfigurationError`][clappform.ConfigurationError] | (pre-flight / missing header) | Bad endpoints, credentials, retry policy or cluster discovery, a closed client, or a call the server rejected for a missing `location` header |
| [`AuthenticationError`][clappform.AuthenticationError] | `UNAUTHENTICATED` | The credential was rejected |
| [`PermissionDeniedError`][clappform.PermissionDeniedError] | `PERMISSION_DENIED` | Authenticated, but not allowed |
| [`NotFoundError`][clappform.NotFoundError] | `NOT_FOUND` | The referenced entity does not exist, including a slug or saved-query name that resolves to nothing |
| [`InvalidRequestError`][clappform.InvalidRequestError] | `INVALID_ARGUMENT` / `FAILED_PRECONDITION` / `OUT_OF_RANGE` | Malformed request or violated precondition |
| [`ConflictError`][clappform.ConflictError] | `ALREADY_EXISTS` / `ABORTED` | Conflicts with existing state |
| [`ResourceExhaustedError`][clappform.ResourceExhaustedError] | `RESOURCE_EXHAUSTED` | A size or rate limit, such as a message over the 64 MiB gRPC cap |
| [`NotSupportedError`][clappform.NotSupportedError] | `UNIMPLEMENTED` | The cluster doesn't serve the RPC (staggered rollouts, or an RPC not implemented yet) |
| [`TransientError`][clappform.TransientError] | `UNAVAILABLE` / `DEADLINE_EXCEEDED` | The server was unreachable or the deadline passed |

A status with no entry above raises `ClappformError` itself. The client also
raises plain `ClappformError` when pandas is missing for a DataFrame call and
when a [`ReadResult`][clappform.ReadResult] is consumed twice.

**`TransientError`** covers two cases. `UNAVAILABLE` means the server could not
be reached or dropped the call; the client has already retried it if it was
a read (see [Retries](#retries)). `DEADLINE_EXCEEDED` means the call ran
past its deadline; it is never retried.

**`ResourceExhaustedError`** usually means one gRPC message passed 64 MiB. Lower
`chunk_rows` on a write or `batch_size` on a read, or raise
`grpc.max_send_message_length` / `grpc.max_receive_message_length` through
`channel_options=`. It can also be a server-side quota or rate limit.

## Errors raised before a call

These come from Python, not the server, and do not derive from
`ClappformError`:

| Exception | Raised when |
|---|---|
| `ValueError` | `append()` or `upsert()` gets a frame with an `_id` column; `append()`, `update()` or `upsert()` gets a frame with a named index; `update()` / `upsert()` get a frame missing the `on` column, or a row whose key is null or NaN; `update_where({})` or `delete(where={})`; `delete()` without exactly one of `where=` / `oids=`; `chunk_rows` below 1; a row or pipeline holds `inf` or `-inf` |
| `TypeError` | A value the codec cannot encode (the message names its type); a generated method given both a request message and field keyword arguments, a message of the wrong type, two members of one `oneof`, or a stream item of the wrong type |
| `NotImplementedError` | `ReadResult.to_arrow()` / `to_polars()`, reserved until the server sends Arrow |
| `AttributeError` | A name that is not on the object, e.g. `cf.insert`; the message names the family that owns it when there is one |

`replace_where()` also emits a `DeprecationWarning`; call `update_where()`.

Exceptions you raise yourself pass through unchanged. An exception raised while
the client produces a request stream, such as one from your `progress`
callback, reaches you as that exception, not as a cancelled call.

## Catching errors

Catch the specific type you can act on and let the rest propagate:

```python
--8<-- "errors_and_retries.py:typed-errors"
```

## Retries

Retries are configured once on the client and applied by gRPC's built-in retry
support. The default, `clappform.DEFAULT_RETRIES`, makes up to 4 attempts on
`UNAVAILABLE`, backing off from 0.2 s to 2 s. Override it per client with a
[`RetryPolicy`][clappform.RetryPolicy], or pass `retries=None` to disable.

```python
--8<-- "errors_and_retries.py:retry-policy"
```

`RetryPolicy` takes backoffs in seconds as floats (the `"0.2s"` string form
still works). `max_attempts` must be between 2 and 5, because gRPC caps it at
5; any other value raises `ConfigurationError` rather than being clamped.

!!! warning "Only reads are retried"
    The policy applies to RPCs whose name starts with a read verb: `Get`,
    `List`, `Read`, `Describe`, `Aggregate`, `Download`, `Health` or `Preview`
    (`clappform._transport.READ_METHOD`). Every other RPC, such as
    `InsertMany`, `SyncManyByField`, `actionflow.start` or
    `transfer.import_app`, runs without one. An `UNAVAILABLE` write or action
    may already have been applied: retrying an `InsertMany` could duplicate
    rows, and retrying a `start` could run the actionflow twice. gRPC's
    transparent retry, for a request that never reached the server, still
    applies to every RPC.

### When `append()` fails partway

`append()` is not idempotent. The rows the server acknowledged before the
failure stay inserted, and the raised error's `rows_written` says how many. A
chunk that was in flight may have been written as well, so `df.iloc[rows_written:]`
is not guaranteed to be the exact remainder. Finish or repeat the load with
`upsert(on=...)`, which converges:

```python
--8<-- "errors_and_retries.py:append-failure"
```

### Retrying a whole flow

When a `TransientError` escapes, re-run the operation from the top if every
step in it is safe to repeat. Reads are, and so is `upsert(on=...)`, because a
second run replaces the same documents. `append()` is not. A small back-off loop
is usually all you need:

```python
--8<-- "errors_and_retries.py:retry-flow"
```

## Deadlines

The client has two default deadlines:

- `timeout=` (default 60 seconds) applies to unary calls: one request, one
  response.
- `stream_timeout=` (default `None`) applies to streaming calls, which include
  every DataFrame read and write. With no deadline, a stream runs as long as it
  keeps moving, and gRPC keepalive (every 30 seconds) detects a dead
  connection.

```python
--8<-- "errors_and_retries.py:deadlines"
```

A `timeout=` on one call overrides both for that call. On a streaming call it
bounds the whole stream, including the time your code spends between chunks.

```python
--8<-- "errors_and_retries.py:per-call-timeout"
```

See the [Errors reference](../reference/errors.md) for the full hierarchy, and
[Troubleshooting & FAQ](troubleshooting.md) for symptom-first fixes.
