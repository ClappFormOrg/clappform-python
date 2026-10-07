# Cookbook

Copy-paste recipes for the tasks people write most. Every block here runs
against `LocalMock` in CI, so the code is known-good. Lift it straight into
your script and swap the collection names and filters for yours.

For the full argument list behind any call, see [DataFrame flows](dataframes.md)
(the collection surface) and the [API families reference](../reference/api-families.md)
(everything on `cf.client` / `cf.data`).

## Collection CRUD

The operations you'll use most, on a `cf.data.collection(ref)` handle.
`ref` is a collection slug or UUID; a slug is resolved once and cached per
location.

!!! warning "Update and delete-by-filter are not served yet"
    `update()` and `delete(where=...)` raise
    [`NotSupportedError`][clappform.NotSupportedError] on every cluster today,
    because the Data Connector does not implement their RPCs yet. The recipes
    below run them against `LocalMock(include_unreleased=True)`. Today, write
    changes back with `upsert(on=...)` and delete with `delete(oids=...)` or
    `clear()`.

### Create (insert new rows)

```python
--8<-- "cookbook.py:crud-create"
```

### Read (filter into a DataFrame)

```python
--8<-- "cookbook.py:crud-read"
```

### Update (write changes back, not served yet)

```python
--8<-- "cookbook.py:crud-update"
```

### Upsert (insert-or-update on a business key)

```python
--8<-- "cookbook.py:crud-upsert"
```

### Delete

```python
--8<-- "cookbook.py:crud-delete"
```

!!! warning "Full wipes are explicit"
    `delete(where={})` is refused, because an empty filter matching every
    document is almost always a bug. To empty a collection on purpose, call `clear()`.

## Read a single record

Filter, cap at one row, and take it as a dict, with an `.empty` guard so a
miss returns `None` instead of raising.

```python
--8<-- "cookbook.py:single-read"
```

## Load a file into a collection

Read the bytes into a DataFrame with pandas, then `append()`.

```python
--8<-- "cookbook.py:ingest-file"
```

pandas picks the reader from the format: `read_csv`, `read_excel` (needs
`openpyxl`), `read_parquet`, `read_json`. The client chunks and streams the
upload; `append()` returns the number of rows the server acknowledged.
`append()` is not idempotent, so running the ingest twice inserts the file
twice. For a load you may re-run, use `upsert(df, on="...")` instead so a
re-run replaces the same documents.

## Aggregate a collection into a DataFrame

Group, sort, or reshape server-side and get a frame back.

```python
--8<-- "cookbook.py:aggregate-to-df"
```

`aggregate(p)` is `read(pipeline=p)` returning a DataFrame, so use whichever
name reads better at the call site. A plain filter/projection is a pipeline
with a `$match`/`$project` stage (see the read recipe above); reach for the
`aggregate()` name when the call is conceptually a grouping or reshape.

## Stream a large aggregation into DataFrames

`aggregate()` and `read()` materialise the **whole** result in memory before
handing it back, which is fine for a slice and wasteful for a result too big to
hold. When you're reducing or writing out row-by-row, stream instead:
`fetch(pipeline=...).iter_batches()` yields one gRPC chunk at a time, so you
convert each chunk to a small DataFrame, fold it into your running result, and
let it be freed before the next arrives. **Peak memory is one batch, not the
whole set.**

```python
--8<-- "cookbook.py:stream-aggregate"
```

`batch_size` caps the rows per chunk: raise it to trade memory for fewer
round-trips, lower it when rows are wide. This is the memory-efficient path for
large aggregations you can process incrementally (summing, writing to a file or
another collection, feeding a model). If you genuinely need the entire result as
one frame, `aggregate()` is simpler; the streaming form only helps when you can
avoid holding it all.

!!! note "A result streams once"
    The [`ReadResult`][clappform.ReadResult] from `fetch()` is single-pass:
    iterate it (or `to_pandas()` it) exactly once. Call `fetch()` again for a
    fresh pass rather than reusing a consumed result.

## Handle an empty result

A read matching nothing returns an empty DataFrame, never an error and never
`None`. It has no columns, so branch on `.empty` before indexing one.

```python
--8<-- "cookbook.py:empty-read"
```

## Write a change-request record

A change request is a row in its own collection.

```python
--8<-- "cookbook.py:change-request"
```

To amend an existing change-request row, match on your own identifier with
`upsert(df, on="cf_original_id")`, sending the whole row. `update()` on its
`_id` will also work once the server serves it.

## Start an actionflow

Trigger a flow by id; the response carries the run's `uuid`.

```python
--8<-- "cookbook.py:actionflow-start"
```

To hand the flow start parameters, pass `custom_keys=`, which takes JSON bytes
today, so encode a dict:

```python
--8<-- "cookbook.py:actionflow-params"
```

More on the in-worker context in
[Running in an actionflow](actionflow-scripts.md), and on listing/inspecting
flows in [Actionflows & listings](actionflows-and-listings.md).

## Manage indexes

Create, list, and drop indexes on a collection through `cf.data.index`.

```python
--8<-- "cookbook.py:index"
```

`create()` also takes a `mongo_index_model=` (for compound or option-bearing
indexes) or `elastic_settings=` for Elastic-backed collections; passing only
`index_name` builds a simple single-field index.

## Move an app between instances

Export an app bundle from the source instance and import it into the
destination. Each part (`app`, `queries`, `actionflows`, `questionnaires`) is
bytes, so it passes straight through.

```python
--8<-- "cookbook.py:transfer"
```

Choose what travels with the `include_*` flags on `export_app`, and set
`overwrite=` on `import_app` to control clobbering an existing app.

## Copy data across clusters

Two clients are two clusters in one process. Read from one and `upsert()` into
the other on a business key so re-runs never duplicate. Drop `_id` first: it
identifies the document on the source cluster, and the target assigns its own.

```python
--8<-- "cookbook.py:cross-cluster"
```

See [Multi-cluster & multi-tenant](multi-cluster.md) for sharing connections
across tenants on the same cluster.
