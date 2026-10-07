# Multi-cluster & multi-tenant

Cluster and location are independent axes. The **cluster** is the host
extension that picks the endpoints: `""` for the main cluster, or another
cluster's extension such as `"qa"` or `"prod-lts"`. `"prod"` is accepted as
another name for the main cluster `""`; it is not `"prod-lts"`. The
**location** is the tenant: it picks the database within those endpoints and is
sent as metadata on every call. Nothing is global, so any combination coexists
in one process.

Each API family has its own host: `data`, `client`, `login` (for `cf.auth`)
and `notify` (for `cf.notifier`). The main cluster serves them on port 50051,
e.g. `data.clappform.com:50051`; every other cluster serves TLS on port 443,
e.g. `data-qa.clappform.com`. Override a family's address with
`endpoints={"data": "host:port"}`.

## Two clusters, one process

Each client is its own binding with its own credentials. Point one at the main
cluster and one at qa and use them side by side:

```python
--8<-- "multi_cluster.py:two-clusters"
```

Omit `cluster=` and the client discovers it from the DNS CNAME of
`{location}.clappform.com`, giving up after 5 seconds. An explicit `cluster=`
always wins, so pass it in air-gapped or split-DNS environments where discovery
can't run.

## Copying across clusters

Because both clients are plain objects, a cross-cluster copy is a read on one
and a write on the other. Drop `_id` before writing: it identifies the document
on the source cluster, and the target assigns its own.

```python
--8<-- "multi_cluster.py:cross-cluster"
```

## Moving a whole app between instances

The copy above moves *rows*. To move an entire **app**, with its collections and,
optionally, its queries, actionflows and questionnaires, use the transfer
RPCs. `export_app()` reads the bundle from the source instance and returns it as
four byte blobs; `import_app()` writes those same blobs into the target. It's
inherently a two-instance operation: read from one client, write to the other.

```python
--8<-- "multi_cluster.py:transfer-app"
```

The `include_*` flags on `export_app()` choose what travels with the app, and
the `AppExport` it returns exposes exactly the `app` / `queries` / `actionflows`
/ `questionnaires` fields `import_app()` consumes, so the hand-off is a direct
pass-through with no reshaping. Pass `overwrite=True` on the import only when you
intend to replace an app that already exists on the target; the default refuses
to clobber it. `export_actionflow()` / `import_actionflow()` move a single
actionflow the same way when you don't need the whole app.

## Another location on the same cluster

`with_location()` gives a cheap clone bound to a different location. When the
cluster is known (explicit, or a custom transport) the clone shares the parent's
connections and configuration: only the location metadata differs, and no DNS
is performed.

```python
--8<-- "multi_cluster.py:with-location"
```

!!! note "Discovered clusters may re-discover"
    If the parent's cluster was *discovered* (no `cluster=`), a different
    location is re-resolved: if it lands on the same cluster the transport is
    still shared, otherwise the clone gets its own transport for its own
    cluster, which you must close. With an explicitly configured cluster,
    `with_location()` never performs DNS. See
    [Client lifecycle](concepts.md#client-lifecycle) for which clone owns
    what.

### Fanning out across many locations

Running the same job across a list of locations is a loop: clone per
location, do the work, move on. Open each clone with `with`, so a clone that
re-discovered another cluster closes its own connections; a clone that shares
the parent's connections ignores the close.

```python
--8<-- "multi_cluster.py:fan-out-tenants"
```

A clone on the parent's cluster reuses the parent's channels, so this doesn't
open a connection per location.

!!! warning "Don't `with` the parent's own location"
    `cf.with_location(cf.location)` returns `cf` itself, not a clone, so
    leaving a `with` block around it closes the parent. Keep the parent's own
    location out of the loop, or use the parent directly for it.

## Staggered rollouts

Clusters update at different times, so a newer client may call an RPC an older
cluster doesn't serve yet. That surfaces as
[`NotSupportedError`][clappform.NotSupportedError] (gRPC `UNIMPLEMENTED`), not a
crash. Handle it where you rely on a just-added RPC; see
[Error handling & retries](errors-and-retries.md).

See the [Client reference](../reference/client.md) for the full constructor and
`with_location()` signature.
