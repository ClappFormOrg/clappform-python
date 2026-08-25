# Migrating from 4.x / 5.x

Version 6 is a full rewrite. If your scripts import `clappform.Data`,
`clappform.Client`, or anything from `clappform.proto.*`, they are on the old
package. This guide shows the v6 way for every common call, with the old form
kept underneath purely as a memory jog.

The short version: the raw protobuf request objects, the manual
`json.dumps(...).encode("utf-8")` around pipelines and payloads, the
`pd.concat([pd.DataFrame(json.loads(x.data)) for x in ...])` read loop, and the
separate `Data` / `Client` objects are all gone. You work with a single
`Clappform` client and pandas DataFrames.

!!! note "How to read this page"
    The **v6** code in each section is what you write now, and it is pulled from
    a snippet that runs against `LocalMock` in CI, so it is known to work.
    The **old 4.x / 5.x** form is tucked into a collapsed "reference" block below
    each one; open it only if you need to recognise what you're replacing.

## Connecting

There were two client classes, `Data` and `Client`, each taking a token, a
location, and often an explicit `target` host:port. v6 has one client, and the
cluster is discovered from DNS.

```python
--8<-- "migrating.py:connect"
```

Data-plane calls that were on `Data` now live on `cf.data`; the ones on
`Client` live on `cf.client`. If you talk to an older cluster that still serves
gRPC on `:50051`, pass it through `endpoints=` (see
[Multi-cluster](multi-cluster.md)). Discovery targets the current clusters on
443.

??? note "Old (4.x / 5.x) reference"

    ```python
    import clappform

    d = clappform.Data(token=TOKEN, location=LOCATION, target="data-test.clappform.com:50051")
    c = clappform.Client(token=TOKEN, location=LOCATION)
    ```

## Reading a collection

`read()` collapses the request object, the hand-encoded pipeline, and the
`pd.concat` over streamed chunks into one call that returns a DataFrame.

```python
--8<-- "migrating.py:read"
```

??? note "Old reference"

    ```python
    from clappform.proto.clappform.data.v1 import aggregate_pb2

    request = aggregate_pb2.AggregateStreamRequest(
        pipeline=json.dumps([{"$match": {"status": "open"}}]).encode("utf-8"),
        collection=COLLECTION,
    )
    df = pd.concat(
        [pd.DataFrame(json.loads(x.data)) for x in d.aggregate(request)],
        ignore_index=True,
    )
    ```

If you had a full pipeline (`$group`, `$sort`, …) rather than a simple filter,
pass it to `aggregate()`, still with no `json.dumps`, no `encode()`, no manual
concat:

```python
--8<-- "migrating.py:aggregate"
```

## Inserting rows

`append()` chunks and streams the upload for you and returns the number of rows
written. No `insert_many_dataframe` helper, no draining the response iterator.

```python
--8<-- "migrating.py:insert"
```

??? note "Old reference"

    ```python
    from clappform.utils import insert_many_dataframe

    request = insert_many_dataframe(collection, df, size=100)
    list(client.insert_many(request))
    ```

## Updating rows

`read()` keeps `_id` on the frame, so you mutate and hand it straight back with
no batching, no per-batch JSON serialisation, no `UpdateRequestByOid`.

```python
--8<-- "migrating.py:update"
```

??? note "Old reference"

    ```python
    for start in range(0, len(df), batch_size):
        batch = df.iloc[start:start + batch_size]
        request = update_pb2.UpdateRequestByOid(
            data=batch.to_json(orient="records").encode("utf-8"),
            collection=collection,
        )
        d.update_replace_many(request)
    ```

## Deleting rows

`delete()` takes exactly one of `oids=` (specific `_id`s) or `where=` (a
filter). An empty `where` is refused; use `clear()` for a deliberate full wipe.

```python
--8<-- "migrating.py:delete"
```

??? note "Old reference"

    ```python
    from clappform.proto.clappform.data.v1 import delete_pb2

    request = delete_pb2.DeleteRequestOids(oids=ids, collection=collection)
    d.delete_many_by_oids(request)
    ```

## Starting an actionflow

`start()` takes an id on the same client, with no raw `StartActionflow` proto, no
integer `actionflowid`, no magic `user=` number.

```python
--8<-- "migrating.py:actionflow"
```

To pass start parameters, use `custom_keys=`. Today that field takes JSON
bytes, so build it with `json.dumps({...}).encode("utf-8")`. See
[Running inside an actionflow](actionflow-scripts.md#passing-start-parameters).

??? note "Old reference"

    ```python
    from clappform.proto.clappform.client.v1 import actionflow_pb2

    request = actionflow_pb2.StartActionflow(
        actionflowid=ACTIONFLOW_ID,
        user=4,
        settings=json.dumps({"custom_keys": {"next_page": NEXT_PAGE}}),
    )
    c.actionflow_start(request)
    ```

## Mapping table

| You had (4.x / 5.x) | You now write (6.x) |
| --- | --- |
| `clappform.Data(token, location, target=...)` | `Clappform(location=..., api_key=...)` → `cf.data` |
| `clappform.Client(token, location)` | the same client → `cf.client` |
| `d.aggregate(AggregateStreamRequest(...))` + `pd.concat(...)` | `cf.data.collection(ref).read(...)` / `.aggregate([...])` |
| `insert_many_dataframe(...)` + `insert_many(...)` | `cf.data.collection(ref).append(df)` |
| `update_replace_many(UpdateRequestByOid(...))` | `cf.data.collection(ref).update(df)` |
| `delete_many_by_oids(DeleteRequestOids(...))` | `cf.data.collection(ref).delete(oids=[...])` |
| `c.actionflow_start(StartActionflow(...))` | `cf.client.actionflow.start(id=...)` |
| `from clappform.proto...import *_pb2` | not needed, though `clappform.gen...` is there if you want the raw stubs |
| manual `json.dumps(pipeline).encode()` | pass Python dicts/lists; the client encodes |
| `try/except grpc.RpcError` | `except ClappformError` (see [Errors](errors-and-retries.md)) |

## Things that moved out of scope

- **HTTP fallback.** The old scripts sometimes hit `client.clappform.com/api/v1`
  with `requests` for endpoints the gRPC client didn't wrap (questionnaires,
  the message API). v6 is gRPC-first; if an operation isn't on a sub-client yet,
  reach for the generated stub under `clappform.gen...` rather than raw HTTP.
- **`target="...:50051"`.** Discovery targets current clusters on 443. Legacy
  `:50051` hosts are reachable via an explicit `endpoints=` override.

Next: the [Cookbook](cookbook.md) for the recipes these building blocks compose
into.
```
