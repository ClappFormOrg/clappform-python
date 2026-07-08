# Troubleshooting & FAQ

Symptom → cause → fix for the things people actually hit. Every code block runs
against `LocalMock` in CI, so the "do this instead" is known-good.

## Connecting

### `ConfigurationError: cannot discover a cluster for location ...`

DNS-based cluster discovery couldn't resolve `{location}.clappform.com` to a
recognised cluster. Common on Alpine/musl containers (which may not return the
canonical name), split-DNS, or air-gapped networks.

**Fix:** pass the cluster explicitly so discovery is skipped:

```python
cf = Clappform(location="acme", cluster="prod", api_key="...")  # no DNS lookup
```

### `AuthenticationError`, or an error mentioning a missing `location` header

The API key was rejected, or the tenant header wasn't sent. `location` is
required on every call and is a constructor argument — the library never reads
it from the environment.

**Fix:** confirm the key is valid for the cluster you landed on, and that
`location` is your tenant subdomain. `repr(cf)` prints both the cluster and
location the client is bound to — check it first:

```python
print(cf)  # Clappform(cluster='prod', location='acme', auth=ApiKey, version=..., protos=...)
```

### `NotSupportedError` (gRPC `UNIMPLEMENTED`)

The cluster you're talking to doesn't serve that RPC **yet**. Clusters roll out
on staggered schedules, so a call that works on one cluster can be unimplemented
on another.

**Fix:** check which cluster you're on (`repr(cf)`), and read the docs for the
version that cluster is running (use the version selector). If you expect the
RPC to exist, the cluster likely hasn't been updated.

## Reading & writing

### `NotFoundError` on a slug I'm sure exists

Usually a typo, the wrong tenant, or the collection was recreated (its slug
remapped to a new id). The error names the slug and the location it searched, so
read the message first. The client already re-resolves a stale cached slug once
automatically; a persistent `NotFoundError` means it genuinely isn't there for
that tenant.

```python
--8<-- "troubleshooting.py:not-found"
```

### "This `ReadResult` has already been consumed"

A result set streams **once** — iterate it or `to_pandas()` it exactly once.
Reusing the same `fetch()` result raises rather than silently returning empty.

```python
--8<-- "troubleshooting.py:consumed-result"
```

### An empty read blows up with `KeyError` on a column

A read that matches nothing returns an empty DataFrame with **no columns**, so
`df["col"]` raises. Branch on `df.empty` before indexing — see
[Handle an empty result](cookbook.md#handle-an-empty-result).

### A big read times out (`TransientError` / `DEADLINE_EXCEEDED`)

The call exceeded the client's default deadline. Raise it for that one call with
`timeout=`, or stream the result in batches instead of materialising it all (see
[Stream a large aggregation](cookbook.md#stream-a-large-aggregation-into-dataframes)).

```python
--8<-- "troubleshooting.py:per-call-timeout"
```

### `inf`/`-inf` can't be encoded when writing

JSON has no representation for infinity, so the codec refuses it rather than
corrupt the payload. Clean the column (`df.replace([np.inf, -np.inf], np.nan)`)
before `append`/`update`. `NaN`/`NaT` are fine — they become JSON `null`.

## Aggregation

### My `$group` pipeline returns raw rows unchanged (in a test)

`LocalMock` runs the `$match`/`$project`/`$limit` stages but does **not** compute
`$group`, `$sort`, `$lookup`, or other stages — it's a transport double, not an
aggregation engine. Stub the grouped answer with `.on()` for that pipeline:

```python
--8<-- "troubleshooting.py:group-in-mock"
```

Against a real cluster the server computes the full pipeline; this only affects
`LocalMock`-based tests.

## FAQ

**How do I read a filtered slice?** Pass an aggregation pipeline:
`col.read(pipeline=[{"$match": {...}}])`. There is no `where=` argument — the
client sends the pipeline verbatim rather than owning a query language.
See [Read & query data](dataframes.md).

**What's the difference between `location` and `cluster`?** `location` is your
tenant (a subdomain, sent on every call); `cluster` is the set of hosts that
serve that tenant. Two tenants can live on the same cluster. See
[Multi-cluster & multi-tenant](multi-cluster.md).

**Slug or UUID?** Both. `collection(ref)`/`query(ref)` take either; a slug is
resolved to its id once and cached per tenant.

**Do I need `grpc` installed / imported to handle errors?** No. Every failure is
a `ClappformError` subclass; you never touch `grpc`. See
[Errors & retries](errors-and-retries.md).

**Which extras do I need?** `clappform[pandas]` for the DataFrame flows (the
recommended install). Core is just `grpcio` + `protobuf`.
