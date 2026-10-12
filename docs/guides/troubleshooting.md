# Troubleshooting & FAQ

Symptom → cause → fix for the things people hit. Every code block runs
against `LocalMock` in CI, so the "do this instead" is known-good.

## Connecting

### `ConfigurationError: cluster discovery failed ...`

When you omit `cluster=`, the client looks up the DNS record of
`{location}.clappform.com` and reads the cluster from its canonical name. The
error says which step failed:

- `cluster discovery failed: could not resolve 'acme.clappform.com' (...); pass cluster= explicitly`:
  the lookup failed. The text in parentheses is the resolver's error, or
  `no DNS answer within 5s` when no answer came back within the 5-second
  limit. Common in air-gapped networks and behind split DNS.
- `cluster discovery failed: 'acme.clappform.com' resolved to canonical name '...', which does not match the expected bigip[-<cluster>].clappform.com convention; pass cluster= explicitly`:
  the lookup answered, but not with a cluster's host. Alpine and other
  musl-based containers return the queried name instead of the canonical one
  and land here.
- `cannot discover a cluster for location '...': not a valid subdomain label; pass cluster= explicitly`:
  `location` contains characters other than letters, digits and `-`.

**Fix:** pass the cluster explicitly so discovery is skipped:

```python
cf = Clappform(location="acme", cluster="", api_key="...")  # "" is the main cluster; no DNS lookup
```

### `AuthenticationError`, or an error mentioning a missing `location` header

The API key was rejected, or the `location` header wasn't usable. A call the server
rejects for its `location` header raises `ConfigurationError` ending in
`the server received no usable tenant header; check the location= argument`.
`location` is required on every call and is a constructor argument; the
library never reads it from the environment.

**Fix:** confirm the key is valid for the cluster you landed on, and that
`location` is your tenant subdomain. `repr(cf)` prints both the cluster and
location the client is bound to, so check it first:

```python
print(cf)  # Clappform(cluster='main' (discovered), location='acme', auth=ApiKey, version=..., protos=...)
```

### `ConfigurationError: client is closed`

The client, or the client a `with_location()` clone shares connections with,
was closed: a `with` block ended or `close()` ran. A closed client stays
closed. **Fix:** create a new client, and keep clones inside the parent's
lifetime. See [Client lifecycle](concepts.md#client-lifecycle).

### `NotSupportedError` (gRPC `UNIMPLEMENTED`)

The cluster you're talking to doesn't serve that RPC. Two causes:

- **The RPC is not implemented yet.** `update()`, `update_where()` and
  `delete(where=...)` call `UpdateMany`, `UpdateManyByField`,
  `UpdateManyByQuery` and `DeleteManyByQuery`, which the Data Connector does
  not serve on any cluster yet. Use `upsert(on=...)`, `delete(oids=...)` or
  `clear()`. `upsert()` on an Elastic-backed collection also answers
  `NotSupportedError`.
- **Staggered rollouts.** Clusters update on different schedules, so a call
  that works on one cluster can be unimplemented on another. Check which
  cluster you're on (`repr(cf)`) and read the docs for the version that
  cluster runs.

## Reading & writing

### `NotFoundError` on a slug I'm sure exists

Usually a typo, the wrong location, or the collection was recreated (its slug
remapped to a new id). The error names the slug and the location it searched,
so read the message first. Collections resolve by **slug**; saved queries
resolve by **name**, so `cf.data.query(...)` needs the query's name, not a
slug. The client re-resolves a stale cached id once; a persistent
`NotFoundError` means it isn't there for that location.

```python
--8<-- "troubleshooting.py:not-found"
```

### "This `ReadResult` has already been consumed"

A result set streams **once**: iterate it or `to_pandas()` it exactly once.
Reusing the same `fetch()` result raises rather than silently returning empty.

```python
--8<-- "troubleshooting.py:consumed-result"
```

### An empty read blows up with `KeyError` on a column

A read that matches nothing returns an empty DataFrame with **no columns**, so
`df["col"]` raises. Branch on `df.empty` before indexing. See
[Handle an empty result](cookbook.md#handle-an-empty-result).

### A read fails with `TransientError` / `DEADLINE_EXCEEDED`

Streaming calls, which include every DataFrame read and write, have no deadline
unless you set one, so this means a `timeout=` on the call or the client's
`stream_timeout=` was shorter than the read. The deadline covers the whole
stream, including time your code spends between batches. **Fix:** raise it for
that call, or leave it unset.

```python
--8<-- "troubleshooting.py:per-call-timeout"
```

A unary call (one request, one response) still gets the client's 60-second
`timeout=` default.

### `ResourceExhaustedError` on a large write or read

One gRPC message passed the 64 MiB limit, usually because rows are wide.
**Fix:** lower `chunk_rows` on `append()` / `upsert()` / `update()`, or
`batch_size` on a read. It can also be a server-side quota or rate limit; the
message says which.

### `ValueError` from `append()` about `_id`

The server assigns ids and rejects inserts that carry `_id`, so `append()`
refuses the frame first. **Fix:** `df.drop(columns="_id")`. To write rows you
read back to the same documents, use `upsert(on=...)` on a business key.

### `inf`/`-inf` can't be encoded when writing

JSON has no representation for infinity, so the codec refuses it rather than
corrupt the payload. Clean the column (`df.replace([np.inf, -np.inf], np.nan)`)
before writing. `NaN`/`NaT` are fine; they become JSON `null`. A value of a
type the codec doesn't know raises `TypeError` naming the type; see
[Type mapping](dataframes.md#type-mapping).

## Aggregation

### "LocalMock does not emulate the '$group' stage" (in a test)

`LocalMock` runs `$match`, `$project`, `$sort`, `$skip` and `$limit`, and raises
on `$group`, `$lookup` and every other stage, because it's a transport double,
not an aggregation engine. Stub the grouped answer with `.on()` for that
pipeline:

```python
--8<-- "troubleshooting.py:group-in-mock"
```

Against a real cluster the server computes the full pipeline; this only affects
`LocalMock`-based tests.

### A `$match` on a date matches nothing

The client sends a `datetime` in a pipeline as an ISO-8601 string, so the
server compares strings. A field stored as a BSON Date never equals a string.
See [Type mapping](dataframes.md#type-mapping).

## FAQ

**How do I read a filtered slice?** Pass an aggregation pipeline:
`col.read(pipeline=[{"$match": {...}}])`. There is no `where=` argument; the
client has no query language of its own and the server runs the pipeline.
See [DataFrame flows](dataframes.md).

**What's the difference between `location` and `cluster`?** `location` is your
tenant (a subdomain, sent on every call); `cluster` is the set of hosts that
serve that tenant. Two locations can live on the same cluster. See
[Multi-cluster & multi-tenant](multi-cluster.md).

**Slug, name or UUID?** `collection(ref)` takes a collection slug or UUID;
`query(ref)` takes a saved query's name or UUID. A slug or name is resolved to
its id once and cached per location.

**Do I need `grpc` installed / imported to handle errors?** No. Every failed
call raises a `ClappformError` subclass; argument mistakes raise `ValueError` or
`TypeError` before a call. See [Error handling & retries](errors-and-retries.md).

**Which extras do I need?** `clappform[pandas]` for the DataFrame flows (the
recommended install). Core is `grpcio` + `protobuf`.
