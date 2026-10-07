# Testing with LocalMock

[`LocalMock`][clappform.testing.LocalMock] is an in-process transport double. It
implements the same transport seam the real client uses, so it plugs straight
into `Clappform(transport=LocalMock())` and every service method works against
it, with no network, no infrastructure, and no keys that matter. Passing
`transport=` also skips DNS discovery, so `cf.cluster` is `None` unless you
name one.

Every example in these guides runs against `LocalMock` in CI, so a doc snippet
that breaks fails the build.

## Seed a data store

`seed(collection, records)` loads records into a collection id, replacing what
was there and giving each record without an `_id` a synthetic one.
`seed_collection_slug(slug, id=...)` registers the slug → id mapping, so
`cf.data.collection(slug)` resolves without a server. Point a client at the
mock and the DataFrame surface round-trips:

```python
--8<-- "testing.py:seed"
```

```python
--8<-- "testing.py:roundtrip"
```

Writes mutate the store, so a follow-up read sees them, which is what lets you
test a read → mutate → write-back pipeline end to end. `records(collection)`
returns a copy of the stored rows for assertions.

## What the built-in handlers cover

| RPC | Behind | Emulation |
|---|---|---|
| `AggregateStream` | `read()`, `fetch()`, `iter_batches()`, `aggregate()`, saved-query reads | The stages listed below; `batch_size` sets the chunk size |
| `InsertSingle`, `InsertMany` | `append()` | Assigns ids; a row carrying `_id` raises `InvalidRequestError`, as the server does |
| `SyncManyByField` | `upsert()` | Updates rows whose key matches, inserts the rest |
| `DeleteManyByOids`, `Clear` | `delete(oids=...)`, `clear()` | |
| `UpdateMany`, `UpdateManyByField`, `UpdateManyByQuery`, `DeleteManyByQuery` | `update()`, `update_where()`, `delete(where=...)` | Raise `NotSupportedError` unless `include_unreleased=True` |

The pipeline emulation runs:

- `$match` on top-level fields, with equality or the operators `$eq`, `$ne`,
  `$gt`, `$gte`, `$lt`, `$lte`, `$in`, `$nin` and `$exists`;
- `$project` with inclusions (`{"field": 1}`), keeping `_id` unless it is set
  to `0`;
- `$sort`, `$skip` and `$limit`.

Any other stage (`$group`, `$lookup`, `$unwind`, ...) or operator (`$or`,
`$regex`, `$elemMatch`, ...) raises `ClappformError` rather than returning rows
the server would not. Stub `AggregateStream` with `.on()` for those pipelines
(see [Stub any other RPC](#stub-any-other-rpc)). Dotted paths are not
resolved: `{"$match": {"address.city": "Utrecht"}}` matches nothing.

!!! note "Where the mock differs from the server"
    The mock's upsert merges the row into the matched record, while the Data
    Connector replaces the matched document with the row. Assert on fields
    the frame carries, not on fields it leaves out.

## RPCs the server does not serve yet

`update()`, `update_where()` and `delete(where=...)` call RPCs the Data
Connector does not implement yet. By default the mock raises
[`NotSupportedError`][clappform.NotSupportedError] for them, as a real
cluster does, so a test cannot pass on a call production would reject. Pass
`include_unreleased=True` to emulate them when you test code written ahead of
the server rollout:

```python
--8<-- "testing.py:unreleased"
```

## Saved queries

`seed_query(name, collection=...)` registers a saved query that reads a
seeded collection, and the name listing that `cf.data.query(name)` resolves
through:

```python
--8<-- "testing.py:saved-query"
```

## Assert on the calls made

The mock records every call on `mock.calls` as a
[`RecordedCall`][clappform.testing.RecordedCall] (`kind`, `method`, `request`,
`timeout`, `metadata`, `location`), which is how you check that the right RPC
ran with the right location and deadline.

```python
--8<-- "testing.py:assert-calls"
```

## Stub any other RPC

The seedable store covers the data plane. For any other RPC, register a canned
response with `on()`, keyed by the full gRPC method path. It may be a response
message, a `handler(request)` callable, or (for a streaming RPC) an iterable of
responses. An explicit stub always wins over a built-in handler, and
registering the same method again replaces the stub.

```python
--8<-- "testing.py:stub"
```

### Make a call fail

A handler stub receives the request (a list of messages for a streaming
upload) and may raise. Raise the client's own exception types, such as
[`NotFoundError`][clappform.NotFoundError] or
[`TransientError`][clappform.TransientError], to drive your error handling:

```python
--8<-- "testing.py:stub-error"
```

## Reset between tests

`reset()` clears recorded calls, stubs, seeded collections, and the slug and
saved-query listings:

```python
--8<-- "testing.py:reset"
```

See the [Testing reference](../reference/testing.md) for every seeding and
stubbing method.
