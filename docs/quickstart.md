# Quickstart

Install, connect, and round-trip a DataFrame in about twenty lines.

## Install

```bash
pip install "clappform[pandas]"
```

The core dependencies are just `grpcio` and `protobuf`. pandas comes in the
`[pandas]` extra, which you want for the DataFrame flows below.

## Connect

A client is one binding: a cluster, a tenant (`location`), and a credential.
Nothing is read from the environment — you pass everything in.

```python
--8<-- "quickstart.py:connect"
```

`cluster` is the host extension (`"prod"`, `"qa"`, `"qa-lts"`, or `""` for the
main cluster). Omit it and the client discovers it from the DNS record of
`{location}.clappform.com`; pass it explicitly in air-gapped or split-DNS
setups. `location` is your tenant subdomain and is sent as metadata on every
call.

API keys are the only credential v6 ships. Keep the key out of source — read it
from your own secret store and pass it in.

## Read, mutate, write back

```python
--8<-- "quickstart.py:roundtrip"
```

That is the whole loop: `read()` gives you a pandas DataFrame with `_id` kept as
a column, you change it with plain pandas, and `update()` writes the changed
rows back — matched on `_id` by default, so the common case needs no arguments.

## Next steps

- [DataFrame flows](guides/dataframes.md) — filtering, batching, append /
  upsert, server-side updates and deletes.
- [Multi-cluster & multi-tenant](guides/multi-cluster.md) — several clusters
  and tenants in one process.
- [Error handling & retries](guides/errors-and-retries.md) — the typed error
  hierarchy and retry configuration.
- [Testing with LocalMock](guides/testing.md) — run your pipelines with no
  infrastructure.
