# DataFrame flows

The DataFrame surface is what you reach for day to day. A
[`CollectionHandle`][clappform.CollectionHandle] holds only a client and a
reference: no connection, no state. Every flow runs over the streaming
data RPCs.

Get one from `cf.data.collection(ref)`, where `ref` is a collection slug or
UUID (resolved once and cached per location).

!!! warning "Three write paths are not served yet"
    `update()`, `update_where()` and `delete(where=...)` call `UpdateMany`,
    `UpdateManyByField`, `UpdateManyByQuery` and `DeleteManyByQuery`. The
    protos declare these RPCs but the Data Connector does not implement them
    yet, so on a real cluster they raise
    [`NotSupportedError`][clappform.NotSupportedError]. `LocalMock` raises the
    same error unless you build it with `LocalMock(include_unreleased=True)`.
    The examples for them below run against that emulation. The paths that
    work today are `append()`, `upsert(on=...)`, `delete(oids=...)` and
    `clear()`.

## Read into a DataFrame

`read()` with no arguments streams the whole collection into pandas. To filter,
project, or reshape, pass an aggregation `pipeline`. Use the syntax the
collection's backend expects: Mongo stages for a Mongo-backed collection,
Elastic DSL for an Elastic-backed one.

```python
--8<-- "dataframes.py:read"
```

`_id` is kept as a column, as a hex string. An empty result yields an empty
frame, never an error, but that frame has no columns, so branch on `df.empty`
before indexing a column. See
[Handle an empty result](cookbook.md#handle-an-empty-result).

!!! note "No client-side query language"
    The client does not interpret or rewrite your stages, and has no `where=`
    or `fields=` arguments. It encodes the pipeline to JSON, converting Python
    values the same way it converts row values (see
    [Type mapping](#type-mapping)), and the server runs it.

### Grouping and reshaping with `aggregate()`

`aggregate()` is the DataFrame-returning twin of `read(pipeline=...)`. Reach
for it when a call is conceptually an aggregation (`$group`, `$sort`, `$lookup`)
rather than a filtered read. The result comes back as a DataFrame (one row per
group here).

```python
--8<-- "dataframes.py:aggregate"
```

`read(pipeline=...)`, `fetch(pipeline=...)` and `aggregate(...)` put the
identical pipeline on the wire and differ only in what they hand back
(a DataFrame, a [`ReadResult`][clappform.ReadResult], and a DataFrame
respectively). Use `fetch()` when you want records or memory-bounded batches
instead of a materialised frame.

### Aggregation via a saved query

When the aggregation is defined server-side as a saved query, you don't write
the pipeline at all. `cf.data.query(ref)` takes the query's **name** or UUID;
the [`QueryHandle`][clappform.QueryHandle] sends only the query id, and the
server runs the query's own collection and pipeline.

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
    `fetch()` returns a single-pass [`ReadResult`][clappform.ReadResult]. Iterate
    it or convert it exactly once. `read()` and `iter_batches()` are
    thin wrappers (`read()` is `fetch().to_pandas()`); call `read()`
    again for a fresh pass rather than reusing a materialised result.
    `ReadResult.to_arrow()` and `to_polars()` are reserved names: they raise
    `NotImplementedError` until the server sends Arrow.

## Insert new rows

`append()` inserts every row of the frame as a new document. It streams the
rows in chunks of `chunk_rows` (default 2500) over one `InsertMany` call and
returns the number of rows the server acknowledged.

```python
--8<-- "dataframes.py:insert"
```

- **The frame must not carry an `_id` column.** The server assigns ids and
  rejects inserts that bring their own, so `append()` raises `ValueError`
  first. Drop it with `df.drop(columns="_id")`.
- **`append()` is not idempotent.** If it fails partway, the chunks the
  server acknowledged stay inserted, and running it again inserts them again.
  The raised `ClappformError` carries `rows_written`, the number of rows the
  server acknowledged before the failure; a chunk in flight at that moment
  may also have been written. For a load you may need to re-run, use
  `upsert(on=...)` on a business key instead.

## Update existing rows

!!! warning "Not served yet"
    `update()` raises [`NotSupportedError`][clappform.NotSupportedError] on
    every cluster today. Use `upsert(on=...)` until the Data Connector serves
    `UpdateMany` and `UpdateManyByField`.

`update()` matches rows on the `on` column, `_id` by default. With `on="_id"`
it sends `UpdateMany`; with any other column it sends `UpdateManyByField`.
Either way it sets the frame's columns on each matched document and leaves the
document's other fields alone. Because `read()` keeps `_id`, a read → mutate →
write-back round-trip needs no `on=`. Only the rows in the frame are sent, so
mutate a filtered slice to touch only those rows.

```python
--8<-- "dataframes.py:update"
```

Every row needs a value for the `on` column: a missing column, or a row whose
key is null or NaN, raises `ValueError` before anything is sent. `update()`
returns the number of rows sent; the server reports no match count.

## Upsert / sync on a business key

`upsert()` keys on a business column instead of `_id`: a document whose `on`
value matches a row is replaced by that row, and unmatched rows are inserted.
The replacement is whole-document, so fields the frame does not carry are
dropped (the document keeps its `_id`); send every field you want to keep. It
has no default and requires `on=`, so the key is always explicit. It sends
`SyncManyByField`, which works today on Mongo-backed collections; an
Elastic-backed collection answers `NotSupportedError`.

```python
--8<-- "dataframes.py:upsert"
```

A row whose key already exists **replaces** the matched document; the rest are
inserted. Re-running the same upsert converges rather than duplicating, which
makes it the right call for a load you may need to repeat and for
cross-cluster or external-source syncs (see
[Multi-cluster & multi-tenant](multi-cluster.md)). Because it replaces:

- send whole rows: a field the frame does not carry is gone from the matched
  document afterwards;
- drop `_id` from a frame you read, with `df.drop(columns="_id")`. The read
  gives `_id` as a hex string, not the stored id.

`upsert()` returns the number of rows sent, and every row needs a value for
`on`, as with `update()`.

## Server-side mutate and delete

!!! warning "Not served yet"
    `update_where()` and `delete(where=...)` raise
    [`NotSupportedError`][clappform.NotSupportedError] on every cluster today.
    `delete(oids=...)` and `clear()` work.

`update_where(where, set_values)` sets fields on every document matching a
filter, and `delete(where=...)` removes them, without rows travelling through
the client. An empty `where` matches every document, so both refuse it with
`ValueError`. `update_where()` replaces `replace_where()`, which still works
but warns and is removed before 6.0.0.

```python
--8<-- "dataframes.py:server-side"
```

`delete()` takes exactly one of `where=` (a filter) or `oids=` (specific
`_id`s). Deleting by id is served today; an empty `oids` list makes no call.

```python
--8<-- "dataframes.py:delete-oids"
```

To wipe a collection use `clear()`, which is separate from `delete()` by design
so a full wipe is never an accident of an empty filter.

```python
--8<-- "dataframes.py:clear"
```

## Type mapping

Rows and pipelines travel as JSON. The client converts Python values on the
way out and unwraps Mongo Extended JSON on the way in:

| Python value | Sent as | Notes |
| --- | --- | --- |
| `None`, `NaN`, `NaT`, `pd.NA` | `null` | |
| `inf`, `-inf` | (refused) | Raises `ValueError`; clean the column first. |
| `datetime`, `date`, `pd.Timestamp` | ISO-8601 string | Not a BSON Date. The offset is kept only for timezone-aware values. |
| numpy scalars and arrays | the matching JSON number, bool or array | Converted with `tolist()`. |
| `Decimal` | float | Loses precision beyond a float. |
| `UUID` | string | |
| `set`, `frozenset` | array | Order is not preserved. |
| `dict`, `list`, `tuple` | object, array | Converted element by element. |
| anything else | (refused) | Raises `TypeError` naming the type. |

| Stored value (Extended JSON) | Read as |
| --- | --- |
| `{"$oid": ...}` | hex string, e.g. the `_id` column |
| `{"$date": ...}` | ISO-8601 string (epoch milliseconds are converted to UTC) |

Two consequences:

- **Dates come back as strings,** not `datetime64`. Parse them with
  `pd.to_datetime(df[col])`.
- **A datetime in a pipeline is a string too.** `{"$match": {"at": {"$gte":
  datetime(...)}}}` sends an ISO-8601 string, so it compares strings. That
  works against values this client wrote (they are strings), and matches
  nothing against a field stored as a BSON Date.

```python
--8<-- "dataframes.py:types"
```

See the [DataFrame surface reference](../reference/dataframes.md) for every
method and argument, and [Actionflows & listings](actionflows-and-listings.md)
for the operations beyond the collection handle: starting actionflows and
listing collections, apps and queries.
