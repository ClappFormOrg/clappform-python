# Testing with LocalMock

[`LocalMock`][clappform.testing.LocalMock] is an in-process transport double. It
implements the same transport seam the real client uses, so it plugs straight
into `Clappform(transport=LocalMock())` and every service method works against
it — no network, no infrastructure, no keys that matter.

Every example in these guides runs against `LocalMock` in CI, so a doc snippet
that breaks fails the build.

## Seed a data store

`seed()` loads records into a named collection, and built-in handlers for the
core data RPCs read and mutate that store through the same JSON codec the real
client uses. Point a client at the mock and the full DataFrame surface
round-trips:

```python
--8<-- "testing.py:seed"
```

```python
--8<-- "testing.py:roundtrip"
```

Writes mutate the store, so a follow-up read sees them — which is what lets you
test a read → mutate → write-back pipeline end to end.

## Assert on the calls made

Every call is recorded on `mock.calls` for assertions — handy for checking the
right RPC was invoked with the right tenant.

```python
--8<-- "testing.py:assert-calls"
```

## Stub any other RPC

The seedable store covers the data plane. For any other RPC, register a canned
response with `on()`, keyed by the full gRPC method path. It may be a response
message, a `handler(request)` callable, or (for a streaming RPC) an iterable of
responses. An explicit stub always wins over a built-in handler.

```python
--8<-- "testing.py:stub"
```

See the [Testing reference](../reference/testing.md) for every seeding and
stubbing method.
