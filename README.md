# Clappform

Python client for the Clappform gRPC APIs. Version 6 is a ground-up rewrite:
the full API surface is generated from the shared proto definitions, with a
hand-written ergonomic layer for DataFrame workflows, multi-cluster
configuration, and typed errors.

> **Status: under active development on the `Major/6` branch.** The published
> 4.x/5.x packages are unrelated to this codebase.

## Install

```bash
pip install clappform[pandas]
```

Core dependencies are `grpcio` and `protobuf` only. The DataFrame flows below
need the `pandas` extra; `polars` and `arrow` are also declared, and
`clappform[all]` pulls in everything.

## Quickstart

A client is one binding — a cluster, a tenant (`location`), and a credential.
Nothing is read from the environment; you pass everything in.

```python
from clappform import Clappform

# The cluster is discovered from DNS, so location and an API key are all you need.
cf = Clappform(location="acme", api_key="cf_live_...")

with cf:
    orders = cf.data.collection("sales_orders")

    # Read a filtered slice straight into a pandas DataFrame.
    df = orders.read(where={"status": "open"}, fields=["order_id", "amount"])

    # Mutate it and write the changed rows back — matched on _id by default.
    df["amount"] *= 1.08
    orders.update(df)
```

`cluster` is the host extension (`"prod"`, `"qa"`, `""` for the main cluster);
omit it and the client discovers it from DNS. `location` is your tenant
subdomain, sent as metadata on every call. Nothing is global, so two clusters
or tenants coexist in one process.

## What you can do

| Task | How |
| --- | --- |
| Read / filter into a DataFrame | `cf.data.collection(ref).read(where=..., fields=..., limit=...)` |
| Aggregate (custom pipeline) | `.aggregate([{"$match": ...}, {"$group": ...}, {"$sort": ...}])` |
| Aggregate (saved query) | `cf.data.query(ref).read()` |
| Insert new rows | `.append(df)` |
| Update existing rows | `.update(df)` (keys on `_id`) |
| Upsert / sync on a business key | `.upsert(df, on="order_id")` |
| Server-side mutate / delete | `.replace_where(where, set_values)` / `.delete(where=...)` / `.clear()` |
| Memory-bounded reads | `.iter_batches(batch_size=...)` |
| Start an actionflow | `cf.client.actionflow.start(id=...)` |
| List collections / apps / queries | `cf.client.collection.iter_get_all()` (and `app`, `query`, `cronjob`) |
| Move a whole app between instances | `src.client.transfer.export_app(...)` → `dst.client.transfer.import_app(...)` |

Errors are typed — every failure derives from `ClappformError` and carries the
call context (method, cluster, location), so you never import `grpc` to handle
one.

## Testing without infrastructure

`LocalMock` is an in-process transport double: seed a data store, point a client
at it, and the full DataFrame surface round-trips with no network. Other RPCs
are stubbed with `.on(method_path, response)`.

```python
from clappform import Clappform
from clappform.testing import LocalMock

mock = LocalMock()
mock.seed_collection_slug("sales_orders", id="so-id")
mock.seed("so-id", [{"order_id": "A-1", "amount": 120.0, "status": "open"}])

with Clappform(location="acme", cluster="prod", api_key="test", transport=mock) as cf:
    assert len(cf.data.collection("sales_orders").read(where={"status": "open"})) == 1
```

## Documentation

Full guides and the generated API reference live at
**[clappform.readthedocs.io](https://clappform.readthedocs.io/)** — quickstart,
DataFrame flows, actionflows & listings, multi-cluster / multi-tenant, error
handling & retries, and testing with `LocalMock`. Every code example in the
guides is a runnable snippet exercised against `LocalMock` in CI, so the docs
can't drift from the client.

## Development

```bash
pip install -e .[dev,pandas]
make generate   # regenerate clappform/gen and clappform/services from protos
make check      # ruff + mypy + pytest
make docs-test  # run the doc snippets, then build the site with --strict
```

Code generation reads the proto definitions from the commons repository at
the tag pinned in `COMMONS_VERSION`. Point `CLAPPFORM_COMMONS_DIR` at a local
clone of commons (defaults to a sibling `../commons` checkout).

Generated code under `src/clappform/gen/` and `src/clappform/services/` is
committed; do not edit it by hand.
