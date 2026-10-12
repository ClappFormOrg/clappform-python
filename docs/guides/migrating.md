# Migrating from 4.x / 5.x

Version 6 is a full rewrite. If your scripts import `clappform.Data`,
`clappform.Client`, or anything from `clappform.proto.*`, they are on the 5.x
gRPC package, which this guide maps call by call. The 4.x line was an HTTP
client (`Clappform(url, username, password)` with `get` / `create` / `update` /
`delete` on resource objects); it has no one-to-one mapping, so start from the
[Quickstart](../quickstart.md) instead.

The short version: the raw protobuf request objects, the manual
`json.dumps(...).encode("utf-8")` around pipelines and payloads, the
`pd.concat([pd.DataFrame(json.loads(x.data)) for x in ...])` read loop, and the
separate `Data` / `Client` objects are all gone. You work with a single
`Clappform` client and pandas DataFrames.

!!! note "How to read this page"
    The **v6** code in each section is what you write now, and it is pulled from
    a snippet that runs against `LocalMock` in CI, so it is known to work.
    The **old 5.x** form is tucked into a collapsed "reference" block below
    each one; open it only if you need to recognise what you're replacing.

## Connecting

5.x had two client classes, `Data` and `Client`, each taking a `token`, a
`location`, and a `target` host:port that defaulted to
`data.clappform.com:50051` for both. v6 has one client, and the cluster is
discovered from DNS.

```python
--8<-- "migrating.py:connect"
```

- **Your token works as `api_key=`.** 5.x sent the token in the `x-api-key`
  metadata header; v6 sends `api_key` in the same header.
- **`target` becomes `cluster`.** The extension in the old host is the
  cluster: `data.clappform.com` is the main cluster (`cluster=""`, or its alias
  `"prod"`), and `data-<ext>.clappform.com` is `cluster="<ext>"`. v6 still
  connects to the main cluster on `:50051`; every other cluster is on TLS port
  443. To keep an exact old host:port, pass it per family with
  `endpoints={"data": "host:port"}`.
- **One client, four families.** Calls that were on `Data` live on `cf.data`;
  those on `Client` live on `cf.client`. v6 sends Client API calls to
  `client[-<ext>].clappform.com`, where 5.x sent them to its `target`.
- **`credentials_fn=None`** (plaintext) becomes `insecure=True`.
- **`options_fn=default_options(...)`** becomes `retries=RetryPolicy(...)` plus
  `channel_options=[...]`. The 5.x default retried `UNAVAILABLE` up to 5
  attempts (0.1 s to 1 s backoff) on every RPC, writes included. v6 makes up to
  4 attempts (0.2 s to 2 s) and never retries data-plane writes. See
  [Retries](errors-and-retries.md#retries).
- **Deadlines.** 5.x passed no gRPC deadline. v6 gives unary calls 60 seconds
  and streams none by default; see [Deadlines](errors-and-retries.md#deadlines).

??? note "Old (5.x) reference"

    ```python
    import clappform

    d = clappform.Data(token=TOKEN, location=LOCATION, target="data.clappform.com:50051")
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

v6 unwraps Mongo Extended JSON on read: `_id` arrives as a hex string and
`$date` values as ISO-8601 strings. See
[Type mapping](dataframes.md#type-mapping).

## Inserting rows

`append()` chunks and streams the upload for you and returns the number of rows
the server acknowledged. It chunks at 2500 rows by default (`chunk_rows=`), the
same default as `insert_many_dataframe(size=2500)`.

```python
--8<-- "migrating.py:insert"
```

Two differences from `insert_many_dataframe`:

- **Datetimes are written as ISO-8601 strings.** `insert_many_dataframe`
  serialised with `DataFrame.to_json(orient="records")`, whose default writes
  datetimes as epoch milliseconds. A collection loaded by both versions holds
  both forms.
- **The frame must not carry `_id`;** `append()` raises `ValueError` if it does.

??? note "Old reference"

    ```python
    from clappform.utils import insert_many_dataframe

    request = insert_many_dataframe(collection, df, size=100)
    list(d.insert_many(request))
    ```

## Updating rows

!!! warning "`update()` is not served yet"
    `update()` calls `UpdateMany` / `UpdateManyByField`, which the Data
    Connector does not implement yet, so it raises
    [`NotSupportedError`][clappform.NotSupportedError] on every cluster today.
    Until then, use `upsert(on=...)` below or the `ReplaceMany` call 5.x used.

5.x's `update_replace_many` called `ReplaceMany`, which replaces each document
by `_id`. v6 generates that RPC as `cf.data.update.replace_many`, with the same
`collection` and `data` fields:

```python
--8<-- "migrating.py:replace-many"
```

`update()` is the DataFrame form you will use once the server serves it.
`read()` keeps `_id` on the frame, so you mutate and hand it straight back with
no batching and no per-batch JSON. It sets only the frame's columns and leaves
the rest of each document alone:

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

## Upserting and filter updates

5.x had no upsert: its stubs had no sync service. v6 adds `upsert(on=...)`,
which inserts-or-replaces keyed on a business column and works today on
Mongo-backed collections:

```python
--8<-- "migrating.py:upsert"
```

5.x reached filter updates only through the raw `d.update_stub.UpdateManyByQuery`.
v6 wraps it as `update_where(where, set_values)`, which the Data Connector does
not serve yet. See [DataFrame flows](dataframes.md#server-side-mutate-and-delete).

## Deleting rows

`delete()` takes exactly one of `oids=` (specific `_id`s) or `where=` (a
filter). An empty `where` is refused; use `clear()` for a deliberate full wipe.

```python
--8<-- "migrating.py:delete"
```

`delete(oids=...)` calls the same `DeleteManyByOids` RPC as 5.x and works
today. `delete(where=...)` calls `DeleteManyByQuery`, which the Data Connector
does not serve yet, so it raises `NotSupportedError`.

??? note "Old reference"

    ```python
    from clappform.proto.clappform.data.v1 import delete_pb2

    request = delete_pb2.DeleteRequestOids(oids=ids, collection=collection)
    d.delete_many_by_oids(request)
    ```

## Listing collections, queries and more

5.x wrapped only `collection_get` and `query_get` (fetch one by id); listings
needed the raw stubs (`c.collection_stub.GetAll(...)`). v6 generates every
listing RPC, with an auto-paginating `iter_*` twin:

```python
--8<-- "migrating.py:listing"
```

`limit` is the page size. `iter_get_all()` requests page 1, 2, 3 and so on and
stops at the first empty page or once it reaches `pagination.pages`. See
[Actionflows & listings](actionflows-and-listings.md).

## Starting an actionflow

`start()` takes the same `id`, `user_id` and `custom_keys` fields as the 5.x
`StartActionflow` message, as keyword arguments on the same client.

```python
--8<-- "migrating.py:actionflow"
```

`custom_keys=` takes JSON bytes, so build it with
`json.dumps({...}).encode("utf-8")`. See
[Writing actionflow tasks](actionflow-scripts.md#passing-start-parameters).

??? note "Old reference"

    ```python
    from clappform.proto.clappform.client.v1 import actionflow_pb2

    request = actionflow_pb2.StartActionflow(
        id=ACTIONFLOW_ID,
        custom_keys=json.dumps({"next_page": NEXT_PAGE}).encode("utf-8"),
    )
    c.actionflow_start(request)
    ```

## Handling errors

5.x let `grpc.RpcError` through. v6 translates the status into a typed
exception, so you never import `grpc`:

```python
--8<-- "migrating.py:errors"
```

| `e.code()` in 5.x | Exception in 6.x |
| --- | --- |
| `UNAUTHENTICATED` | `AuthenticationError` |
| `PERMISSION_DENIED` | `PermissionDeniedError` |
| `NOT_FOUND` | `NotFoundError` |
| `INVALID_ARGUMENT`, `FAILED_PRECONDITION`, `OUT_OF_RANGE` | `InvalidRequestError` |
| `ALREADY_EXISTS`, `ABORTED` | `ConflictError` |
| `RESOURCE_EXHAUSTED` | `ResourceExhaustedError` |
| `UNIMPLEMENTED` | `NotSupportedError` |
| `UNAVAILABLE`, `DEADLINE_EXCEEDED` | `TransientError` |
| anything else | `ClappformError` |

A server error about a missing `location` header becomes `ConfigurationError`.
All of these derive from `ClappformError`. See
[Error handling & retries](errors-and-retries.md).

## Mapping table

| You had (5.x) | You now write (6.x) |
| --- | --- |
| `clappform.Data(token, location, target=...)` | `Clappform(location=..., api_key=token)` → `cf.data` |
| `clappform.Client(token, location)` | the same client → `cf.client` |
| `d.aggregate(AggregateStreamRequest(...))` + `pd.concat(...)` | `cf.data.collection(ref).read(...)` / `.aggregate([...])` |
| `insert_many_dataframe(...)` + `insert_many(...)` | `cf.data.collection(ref).append(df)` |
| `d.update_replace_many(UpdateRequestByOid(...))` | `cf.data.update.replace_many(...)` today; `cf.data.collection(ref).update(df)` once served |
| `d.delete_many_by_oids(DeleteRequestOids(...))` | `cf.data.collection(ref).delete(oids=[...])` |
| `c.actionflow_start(StartActionflow(...))` | `cf.client.actionflow.start(id=...)` |
| `c.collection_get(Read(id=...))` / `c.query_get(...)` | `cf.client.collection.get(id=...)` / `cf.client.query.get(id=...)` |
| `c.collection_stub.GetAll(...)` | `cf.client.collection.iter_get_all()` |
| `from clappform.proto...import *_pb2` | not needed, though `clappform.gen...` holds the raw messages |
| manual `json.dumps(pipeline).encode()` | pass Python dicts/lists; the client encodes |
| `try/except grpc.RpcError` | `except ClappformError` (see [Errors](errors-and-retries.md)) |

## Things that moved out of scope

- **HTTP fallback.** Scripts that called `client.clappform.com/api/v1` with
  `requests` for endpoints the gRPC client didn't wrap should look for the RPC
  on a v6 family first; v6 generates a method for every RPC in the four API families.
- **The license** changes from MIT (5.x) to Apache 2.0.

Next: the [Cookbook](cookbook.md) for the recipes these building blocks compose
into.
