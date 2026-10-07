# API families

The four API families hang off the client: `cf.data`, `cf.client`, `cf.auth`,
and `cf.notifier`. Each is a generated sub-client with one attribute per proto
service (`cf.data.insert`, `cf.client.actionflow`, ...) and one method per RPC.
The generator writes these wrappers from the compiled protos, and the
reference pages render their docstrings:

- [Data: `cf.data`](api-data.md)
- [Client: `cf.client`](api-client.md)
- [Authoriser: `cf.auth`](api-auth.md)
- [Notifier: `cf.notifier`](api-notifier.md)

Each method's docstring gives the RPC path and its call kind
(unary-unary, unary-stream, stream-unary or stream-stream). The summary above
it is the RPC's proto comment, or the grpc-gateway OpenAPI summary when the
proto has none, and the `Args:` list holds the request fields' proto comments.
Those comments are as complete as the protos make them: a field without a
comment is not listed, and a terse comment stays terse.

For the everyday DataFrame flows on `cf.data`, prefer the
[DataFrame surface](dataframes.md) (`cf.data.collection(...)` /
`cf.data.query(...)`); the per-RPC methods are the full generated surface
underneath it.

## Calling convention

Every generated method follows the same rules.

**Request: a message or keyword arguments.** Pass a prebuilt request message as
the first argument, or pass its fields as keyword arguments, not both:

```python
--8<-- "calling_convention.py:message-or-kwargs"
```

Mixing the two, or passing a message of the wrong type, raises `TypeError`.
Keyword arguments left at `None` are not set. A field whose type is a message
also takes a `dict`, and an enum field takes the enum's number or name.

**Per-call options.** `timeout=` (seconds), `metadata=` (extra
`(key, value)` headers) and `location=` (a different location for this call
only) are reserved on every method and never name a request field. A field
whose name collides with one of them, or with a Python keyword, takes a trailing
underscore:

```python
--8<-- "calling_convention.py:underscore"
```

**`oneof` fields.** Setting two members of one `oneof` raises `TypeError`
before any call, rather than keeping the last one:

```python
--8<-- "calling_convention.py:oneof"
```

**Streams.** A method whose RPC streams requests takes an iterable of request
messages and checks each item's type. A method whose RPC streams responses
returns an iterator; stop iterating early (`break`, an exception, dropping the
iterator) and the client cancels the call. An exception raised while the
client draws from your request iterable reaches you unchanged.

**Pagination.** A method whose RPC takes a page request and returns a
`pagination` message has an `iter_` twin that yields items across every page.
See [How listings page](../guides/actionflows-and-listings.md#how-listings-page).

**Errors.** A failed call raises a typed
[`ClappformError`](errors.md) subclass, never a `grpc.RpcError`.
