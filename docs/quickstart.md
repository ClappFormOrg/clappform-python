# Quickstart

Install, connect, and round-trip a DataFrame in about twenty lines, then see
the shape almost every real task takes.

Coming from the 4.x or 5.x package? Start with the
[Migrating from 4.x / 5.x](guides/migrating.md) guide instead. It maps every
old call to its v6 equivalent.

## Install

```bash
pip install --pre "clappform[pandas]"
```

Version 6 is in pre-release, so `--pre` is required. Drop it and pip resolves to
4.x, an unrelated HTTP-era package with none of this API.

The core dependencies are just `grpcio` and `protobuf`. pandas comes in the
`[pandas]` extra, which you want for the DataFrame flows below.

## Connect

A client is one binding: a cluster, a tenant (`location`), and a credential.
Nothing is read from the environment; you pass everything in.

```python
--8<-- "quickstart.py:connect"
```

`cluster` is the host extension (`"prod"`, `"qa"`, `"qa-lts"`, or `""` for the
main cluster). Omit it and the client discovers it from the DNS record of
`{location}.clappform.com`; pass it explicitly in air-gapped or split-DNS
setups. `location` is your tenant subdomain and is sent as metadata on every
call.

API keys are the only credential v6 ships. Keep the key out of source. The
library never reads the environment for you, so pull it from your own secret
store and pass it in:

```python
--8<-- "quickstart.py:connect-env"
```

## Read, mutate, write back

```python
--8<-- "quickstart.py:roundtrip"
```

That is the whole loop: `read()` gives you a pandas DataFrame with `_id` kept as
a column, you change it with plain pandas, and `update()` writes the changed
rows back, matched on `_id` by default, so the common case needs no arguments.

!!! tip "Slugs and UUIDs both work"
    `cf.data.collection("sales_orders")` takes a slug or a UUID. A slug is
    resolved to its id once and cached per tenant, so you never paste UUIDs into
    a script to save a lookup.

## A complete task, end to end

Almost every job has the same shape: connect, read a slice, transform it with
plain pandas, write it back, and often kick off a downstream flow. Here is the
whole thing, which is what a real script looks like once the boilerplate is
gone.

```python
--8<-- "quickstart.py:full-task"
```

Running it prints:

```text
pulled 2 open orders
started run run-abc123
```

No request objects, no `json.dumps(...).encode()`, no manual pagination, no
`grpc` imports. The client absorbs all of it.

## What you just did

- **Connected** with one `(cluster, location, credential)` binding. Nothing is
  global, so two clusters or tenants can coexist in one process.
- **Read** a filtered slice straight into pandas over a streaming RPC.
- **Wrote** the changed rows back, matched on `_id`.
- **Started** a second-API call (the Client API) through the same client.
- **Stayed typed.** Any failure would have raised a `ClappformError`
  subclass carrying the cluster and tenant, never a raw `grpc.RpcError`.

## Next steps

- [Migrating from 4.x / 5.x](guides/migrating.md): old call → new call, for
  every operation the previous package had.
- [Cookbook](guides/cookbook.md): copy-paste recipes for the tasks people
  write most: file ingest, aggregation, change requests, cross-cluster copy.
- [DataFrame flows](guides/dataframes.md): filtering, batching, append /
  upsert, server-side updates and deletes.
- [Running inside an actionflow](guides/actionflow-scripts.md): the in-worker
  context: where `location` and the key come from, and passing start parameters.
- [Multi-cluster & multi-tenant](guides/multi-cluster.md): several clusters
  and tenants in one process.
- [Error handling & retries](guides/errors-and-retries.md): the typed error
  hierarchy and retry configuration.
- [Testing with LocalMock](guides/testing.md): run your pipelines with no
  infrastructure.
```
