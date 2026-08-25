# Multi-cluster & multi-tenant

Cluster and tenant are independent axes. The **cluster** (the host extension:
`""`, `"qa"`, `"qa-lts"`, `"prod"`, …) picks the endpoints. The **tenant**
(`location`) picks the database within them and is sent as metadata on every
call. Nothing is global, so any combination coexists in one process.

## Two clusters, one process

Each client is its own binding with its own credentials. Point one at prod and
one at qa and use them side by side:

```python
--8<-- "multi_cluster.py:two-clusters"
```

Omit `cluster=` and the client discovers it from the DNS CNAME of
`{location}.clappform.com`. An explicit `cluster=` always wins, so pass it in
air-gapped or split-DNS environments where discovery can't run.

## Copying across clusters

Because both clients are just objects, a cross-cluster copy is a read on one and
a write on the other:

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

## Another tenant on the same cluster

`with_location()` gives a cheap clone bound to a different tenant. When the
cluster is known (explicit, or a custom transport) the clone shares the parent's
connections and configuration: only the tenant metadata differs, and no DNS is
performed.

```python
--8<-- "multi_cluster.py:with-location"
```

!!! note "Discovered clusters may re-discover"
    If the parent's cluster was *discovered* (no `cluster=`), a different
    location is re-resolved: if it lands on the same cluster the transport is
    still shared, otherwise the clone gets its own transport for its own
    cluster. With an explicitly configured cluster, `with_location()` never
    performs DNS.

### Fanning out across many tenants

Because `with_location()` is cheap and shares connections, running the same job
across a list of tenants is just a loop: clone per tenant, do the work, move
on. Only the tenant metadata changes between iterations.

```python
--8<-- "multi_cluster.py:fan-out-tenants"
```

Each clone reuses the parent's channels (same cluster), so this doesn't open a
connection per tenant. If the tenants span *different* clusters, construct a
`Clappform` per cluster instead. See [two clusters, one process](#two-clusters-one-process).

## Staggered rollouts

Clusters update at different times, so a newer client may call an RPC an older
cluster doesn't serve yet. That surfaces as
[`NotSupportedError`][clappform.NotSupportedError] (gRPC `UNIMPLEMENTED`), not a
crash. Handle it where you rely on a just-added RPC; see
[Error handling & retries](errors-and-retries.md).

See the [Client reference](../reference/client.md) for the full constructor and
`with_location()` signature.
