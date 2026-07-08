# Clappform Python Client

The Python client for the Clappform gRPC APIs. One package, one `Clappform`
client, first-class pandas DataFrame flows, and native multi-cluster /
multi-tenant support.

```python
from clappform import Clappform

# The cluster is discovered from DNS — location and an API key are all you need.
cf = Clappform(location="acme", api_key="cf_live_...")
df = cf.data.collection("sales_orders").read(pipeline=[{"$match": {"status": "open"}}])
```

## What this client is

- **DataFrame-first.** Reads stream straight into pandas; writes take a
  DataFrame back. See [DataFrame flows](guides/dataframes.md).
- **Nothing global.** Every client is one `(cluster, location, credentials)`
  binding — two clusters coexist in one process. The library reads no config
  files and no environment variables; everything is a constructor argument.
- **Generated from the protos.** The API reference is generated from the
  wrapper layer's docstrings, which come from the proto comments, so a new RPC
  appears in these docs in the same release that adds it to the client.
- **Typed errors.** Every failure derives from `ClappformError` and carries the
  call context (method, cluster, location) — you never import `grpc` to handle
  one. See [Error handling & retries](guides/errors-and-retries.md).
- **Testable without infrastructure.** `LocalMock` is an in-process transport
  double; the examples in these guides run against it in CI. See
  [Testing with LocalMock](guides/testing.md).

## Install

```bash
pip install "clappform[pandas]"
```

The core install pulls only `grpcio` and `protobuf`; pandas ships in the
`[pandas]` extra so the DataFrame surface is available.

## Reading these docs

!!! note "Read the docs for your version"
    Clusters roll out on staggered schedules, so a client that talks to one
    cluster may be a different version than one talking to another. Use the
    version selector to read the docs for the client version you are actually
    running. The 4.x HTTP-era docs remain archived under their version tag.

Start with the [Quickstart](quickstart.md), then reach for the how-to guides
for a specific flow. The [Reference](reference/client.md) is the generated,
exhaustive surface.
