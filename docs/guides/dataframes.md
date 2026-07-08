# DataFrame flows

The DataFrame surface is what you reach for day to day. A
[`CollectionHandle`][clappform.CollectionHandle] holds only a client and a
reference — no connection, no state — and every flow runs over the streaming
data RPCs.

Get one from `cf.data.collection(ref)`, where `ref` is a slug or a UUID
(resolved once and cached per tenant).

## Read into a DataFrame

`read()` with no arguments streams the whole collection into pandas. To filter,
project, or reshape, pass an aggregation `pipeline` — the client sends it to the
server untouched, so use the syntax the collection's backend expects (Mongo
stages for a Mongo-backed collection, Elastic DSL for an Elastic-backed one).

```python
--8<-- "dataframes.py:read"
```

`_id` is kept as a column so the frame round-trips through `update()`. An empty
result yields an empty frame, never an error — but that frame has no columns, so
branch on `df.empty` before indexing a column. See
[Handle an empty result](cookbook.md#handle-an-empty-result).

!!! note "No client-side query language"
    The pipeline is passed through verbatim — the client neither interprets nor
    rewrites your stages. There is one read idiom (a pipeline), so there is
    nothing to remember about which operators are "supported": whatever the
    server understands, you can send.

### Grouping and reshaping with `aggregate()`

`aggregate()` is the DataFrame-returning twin of `read(pipeline=...)` — reach
for it when a call is conceptually an aggregation (`$group`, `$sort`, `$lookup`)
rather than a filtered read. The stages are sent to the server untouched and the
result comes back as a DataFrame (one row per group here).

```python
--8<-- "dataframes.py:aggregate"
```

`read(pipeline=...)`, `fetch(pipeline=...)` and `aggregate(...)` put the
identical pipeline on the wire — they differ only in what they hand back
(a DataFrame, a [`ReadResult`][clappform.ReadResult], and a DataFrame
respectively). Use `fetch()` when you want records or memory-bounded batches
instead of a materialised frame.

### Aggregation via a saved query

When the aggregation is defined server-side as a saved query, you don't write
the pipeline at all — the [`QueryHandle`][clappform.QueryHandle] carries its own
collection and pipeline, so you just read it.

```python
--8<-- "dataframes.py:aggregate-query"
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

## Insert new rows

`append()` inserts every row of the frame as a brand-new document and returns
the number of rows written. Uploads stream in chunks, so a failed chunk is
retryable at the flow level rather than a whole-frame resend.

```python
--8<-- "dataframes.py:insert"
```

## Update existing rows

`update()` matches on `_id` by default — the column `read()` keeps — so a
read → mutate → write-back round-trip needs no arguments. Only the rows in the
frame you pass are sent, so mutate a filtered slice to touch just those rows.

```python
--8<-- "dataframes.py:update"
```

## Upsert / sync on a business key

`upsert()` inserts-or-updates keyed on a business column instead of `_id`. It
has no default — you must pass `on=` — so the key is always explicit. This is
the sync primitive: rows whose key already exists are updated in place, the
rest are inserted, and re-running it never creates duplicates. It's what a
cross-cluster or external-source sync builds on (see
[Multi-cluster & multi-tenant](multi-cluster.md)).

```python
--8<-- "dataframes.py:upsert"
```

## Server-side mutate and delete

When you don't need the rows client-side, `replace_where()` and `delete()` run
entirely on the server — nothing is round-tripped through the client. `delete()`
takes exactly one of `where=` (a filter) or `oids=` (specific `_id`s); an empty
`where` is refused.

```python
--8<-- "dataframes.py:server-side"
```

To wipe a collection use `clear()`, which is separate from `delete()` by design
so a full wipe is never an accident of an empty filter.

```python
--8<-- "dataframes.py:clear"
```

See the [DataFrame surface reference](../reference/dataframes.md) for every
method and argument, and [Actionflows & listings](actionflows-and-listings.md)
for the operations beyond the collection handle — starting actionflows and
listing collections, apps and queries.
