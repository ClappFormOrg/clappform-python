# Changelog

The client pins the `commons` proto repo by git tag, so every release records
the proto version it was generated against — a client's behaviour is a function
of both its own version and the protos it wraps. `clappform.__proto_version__`
reports the pinned proto tag at runtime, and `repr(client)` includes it.

!!! note "Per-release entries"
    Release entries — including each release's proto diff — are published from
    the release workflow that also pushes to PyPI, so this page fills in as
    versions ship. The versions below track the 6.x line; the 4.x HTTP-era docs
    remain archived under their own version tag.

## 6.0.0 (alpha)

The greenfield rewrite. One package covering every Clappform gRPC API,
generated from the `commons` protos, with:

- A single `Clappform` client, one binding per `(cluster, location,
  credentials)`, with namespaced sub-clients (`data`, `client`, `auth`,
  `notifier`).
- First-class pandas DataFrame flows (`read` / `append` / `update` / `upsert` /
  `replace_where` / `delete`) and saved-query reads. Reads take an aggregation
  `pipeline` (or none, for the whole collection); the client sends it verbatim
  and never interprets a query language of its own. `aggregate(p)` is the
  DataFrame-returning twin of `read(pipeline=p)`.
- Native multi-cluster / multi-tenant support with optional DNS-based cluster
  discovery.
- A typed error hierarchy that never leaks `grpc` to the caller.
- `LocalMock`, an in-process transport double for testing without
  infrastructure.

Configuration is constructor-only (no config files, no environment lookup) and
API-key auth is the only credential shipped in this line. Async, JWT/SSO auth,
the `nbflow` API, and Arrow/Polars output surfaces are designed-for but not yet
shipped.
