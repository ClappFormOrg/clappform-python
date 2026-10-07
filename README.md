# Clappform

Python client for the Clappform gRPC APIs. Version 6 is a ground-up rewrite:
the full API surface is generated from the shared proto definitions, with a
hand-written ergonomic layer for DataFrame workflows, multi-cluster
configuration, and typed errors.

> **Status: under active development on the `Major/6` branch.** The published
> 4.x/5.x packages are unrelated to this codebase.

## Install

```bash
pip install --pre "clappform[pandas]"
```

Requires Python 3.10 or newer. Version 6 is in pre-release, so `--pre` is
required. Without it pip resolves to the unrelated 4.x package noted above.
Quote the extra so zsh does not glob it.

Core dependencies are `grpcio` and `protobuf` only. The DataFrame flows below
need the `pandas` extra. The `polars` and `arrow` extras are declared, but
`ReadResult.to_arrow()` and `to_polars()` raise `NotImplementedError` in this
release: the server does not send Arrow yet. `clappform[all]` pulls in every
extra.

## Quickstart

A client is one binding: a cluster, a tenant (`location`), and a credential.
Nothing is read from the environment; you pass everything in.

```python
from clappform import Clappform

# The cluster is discovered from DNS, so location and an API key are all you need.
with Clappform(location="acme", api_key="cf_live_...") as cf:
    orders = cf.data.collection("sales_orders")

    # Read a filtered slice into a pandas DataFrame with an aggregation pipeline.
    df = orders.read(pipeline=[{"$match": {"status": "open"}}, {"$limit": 1000}])

    # Change it and write it back, keyed on a business column.
    df["amount"] *= 1.08
    orders.upsert(df.drop(columns="_id"), on="order_id")
```

`upsert(on=...)` replaces each matched document with its row, so write back
whole rows: a `$project` before an upsert drops the fields it leaves out.
`update(df)`, which matches on `_id` and sets only the frame's columns, is not
served by the Data Connector yet and raises `NotSupportedError` on every
cluster today.

`cluster` is the host extension: `""` for the main cluster (`"prod"` is an
alias for it), or e.g. `"qa"` or `"prod-lts"`. Omit it and the client discovers
it from DNS. `location` is your tenant subdomain, sent as metadata on every
call. Nothing is global, so two clusters or tenants coexist in one process.

## What you can do

| Task | How |
| --- | --- |
| Read / filter into a DataFrame | `cf.data.collection(ref).read(pipeline=[{"$match": ...}, {"$project": ...}, {"$limit": n}])` |
| Aggregate (custom pipeline) | `.aggregate([{"$match": ...}, {"$group": ...}, {"$sort": ...}])` |
| Aggregate (saved query) | `cf.data.query(name).read()` |
| Insert new rows | `.append(df)` (the frame must not carry `_id`) |
| Upsert / sync on a business key | `.upsert(df, on="order_id")` |
| Delete rows / wipe a collection | `.delete(oids=[...])` / `.clear()` |
| Not served yet (`NotSupportedError`) | `.update(df)`, `.update_where(where, set_values)`, `.delete(where=...)` |
| Memory-bounded reads | `.iter_batches(batch_size=...)` |
| Start an actionflow | `cf.client.actionflow.start(id=...)` |
| List collections / apps / queries | `cf.client.collection.iter_get_all()` (and `app`, `query`, `cronjob`) |
| Move a whole app between instances | `src.client.transfer.export_app(...)` → `dst.client.transfer.import_app(...)` |

Failed calls raise a typed `ClappformError` subclass carrying the call context
(method, cluster, location), so you never import `grpc` to handle one. Argument
mistakes raise the standard `ValueError` and `TypeError` before any call is
made.

## Testing without infrastructure

`LocalMock` is an in-process transport double: seed a data store, point a client
at it, and the DataFrame surface round-trips with no network. Other RPCs
are stubbed with `.on(method_path, response)`.

```python
from clappform import Clappform
from clappform.testing import LocalMock

mock = LocalMock()
mock.seed_collection_slug("sales_orders", id="so-id")
mock.seed("so-id", [{"order_id": "A-1", "amount": 120.0, "status": "open"}])

with Clappform(location="acme", api_key="test", transport=mock) as cf:
    df = cf.data.collection("sales_orders").read(pipeline=[{"$match": {"status": "open"}}])
    assert len(df) == 1
```

## Documentation

Full guides and the generated API reference live at
**[clappform.readthedocs.io](https://clappform.readthedocs.io/)**: quickstart,
DataFrame flows, actionflows & listings, multi-cluster / multi-tenant, error
handling & retries, and testing with `LocalMock`. Every code example in the
guides, and every Python block in this README, runs against `LocalMock` in CI.

## Development

```bash
pip install -e ".[dev,pandas]"
make generate   # regenerate clappform/gen and clappform/services from protos
make check      # ruff + mypy + pytest
make docs-test  # run the doc snippets, then build the site with --strict
make audit      # pip-audit the installed tree against the advisory databases
make apicheck   # public API removals and signature changes vs origin/Major/6
```

Code generation reads the proto definitions from the commons repository at
the tag pinned in `COMMONS_VERSION`. Point `CLAPPFORM_COMMONS_DIR` at a local
clone of commons (defaults to a sibling `../commons` checkout).

Generated code under `src/clappform/gen/` and `src/clappform/services/` is
committed; do not edit it by hand.

## License

Apache License 2.0. See [LICENSE](LICENSE).

Generated stubs under `src/clappform/gen/google/` and
`src/clappform/gen/grpc/` come from googleapis (Apache-2.0) and grpc-gateway
(BSD-3-Clause); [NOTICE](NOTICE) carries their terms.
