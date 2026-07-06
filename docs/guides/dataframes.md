# DataFrame flows

The DataFrame surface is what you reach for day to day. A
[`CollectionHandle`][clappform.CollectionHandle] holds only a client and a
reference — no connection, no state — and every flow runs over the streaming
data RPCs.

Get one from `cf.data.collection(ref)`, where `ref` is a slug or a UUID
(resolved once and cached per tenant).

## Read into a DataFrame

`read()` streams the collection (or a filtered slice) into pandas. `where`,
`fields` and `limit` are client-side sugar compiled into a
`$match` / `$project` / `$limit` pipeline — the API never sees the kwargs.

```python
--8<-- "dataframes.py:read"
```

`_id` is kept as a column so the frame round-trips through `update()`. An empty
result yields an empty frame, never an error.

### Aggregation the sugar doesn't cover

For stages `where` / `fields` / `limit` don't emit — `$group`, `$sort`, or an
Elastic-backed collection's DSL — pass a full pipeline with `aggregate()`. It is
sent through untouched.

```python
--8<-- "dataframes.py:aggregate"
```

### Memory-bounded reads

For a result set too big to hold at once, `iter_batches()` yields one list of
records per gRPC chunk. `batch_size` asks the server to cap each chunk.

```python
--8<-- "dataframes.py:batches"
```

!!! note "A read streams once"
    `fetch()` returns a [`ReadResult`][clappform.ReadResult] that is single-pass
    — iterate it or convert it exactly once. `read()` and `iter_batches()` are
    thin wrappers (`read()` is literally `fetch().to_pandas()`); call `read()`
    again for a fresh pass rather than reusing a materialised result.

## Write back

`update()` matches on `_id` by default; `append()` inserts new rows; `upsert()`
inserts-or-updates on a business key (which has no default — you must pass
`on=`). Uploads stream in chunks, so a failed chunk is retryable at the flow
level rather than a whole-frame resend.

```python
--8<-- "dataframes.py:write"
```

## Server-side mutate and delete

When you don't need the rows client-side, `replace_where()` and `delete()` run
entirely on the server — nothing is round-tripped through the client. To wipe a
collection use `clear()`, which is explicit by design so a full delete is never
an accident of an empty filter.

```python
--8<-- "dataframes.py:server-side"
```

## Saved queries

A saved server-side query carries its own collection and pipeline, so a
[`QueryHandle`][clappform.QueryHandle] is read-only: `cf.data.query(ref)` where
`ref` is the query's name or UUID.

```python
--8<-- "dataframes.py:saved-query"
```

See the [DataFrame surface reference](../reference/dataframes.md) for every
method and argument.
