# Performance & large datasets

The DataFrame flows are tuned for the common case by default. This page is
for when the data is large enough that *how* you read and write starts to
matter: big reads, bulk loads, and memory pressure.

## Reads: `batch_size` and streaming

`read()` / `aggregate()` **materialise the whole result** in memory before
handing it back. That's fine up to a point; past it, two levers help.

**`batch_size`** caps the rows the server puts in each gRPC chunk. Bigger means
fewer round-trips (faster, more memory held per chunk); smaller means a leaner
peak. Tune it to your row width, not a magic number.

```python
--8<-- "performance.py:read-batch-size"
```

**Stream instead of materialise.** If you're reducing or writing out
row-by-row, don't build one giant DataFrame. Iterate batches and let each fall
out of scope, so peak memory is one chunk:

```python
--8<-- "performance.py:stream-not-materialise"
```

This is the same technique as the
[Stream a large aggregation](cookbook.md#stream-a-large-aggregation-into-dataframes)
recipe: use it whenever the result doesn't need to exist as one frame.

## Writes: `chunk_rows` and progress

`append` / `update` / `upsert` stream the upload in chunks of `chunk_rows`
(default 2500), so no single gRPC message carries the whole frame. Raise it to
trade memory for fewer round-trips; lower it for very wide rows, or when a
write fails with `ResourceExhaustedError` (a message over 64 MiB).

`append` takes a `progress` callback to surface a running count, handy for a
notebook bar or a log line on a long load. It's called with the cumulative
number of rows the server has acknowledged, after each chunk. `update` and
`upsert` take no callback; they return the number of rows sent.

```python
--8<-- "performance.py:write-progress"
```

## Choosing between read paths

| You want | Use |
|---|---|
| The whole (small) result as a frame | `read()` / `aggregate([...])` |
| A large result you reduce/write incrementally | `fetch(...).iter_batches()` |
| A filtered/projected slice | `read(pipeline=[{"$match": ...}, ...])` |
| A prewritten server-side aggregation | `cf.data.query(ref).read()` |

Prefer a **saved query** over an ad-hoc pipeline when the same aggregation runs
repeatedly: it lives server-side, so the client sends only its id and every
caller runs the same pipeline. Reach for an ad-hoc `pipeline=` when the shape
is one-off or computed at runtime.

## Rules of thumb

- Default `batch_size` / `chunk_rows` are fine until profiling says otherwise;
  don't tune preemptively.
- Memory-bound? Stream (`iter_batches`) rather than raising `batch_size`.
- Throughput-bound on a bulk load? Raise `chunk_rows` so there are fewer chunks.
- Reads and writes stream with no deadline by default. If you set `timeout=`
  or `stream_timeout=`, it bounds the whole stream, batches included. See
  [Deadlines](errors-and-retries.md#deadlines).
