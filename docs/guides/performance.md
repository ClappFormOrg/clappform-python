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
(default 2500), so a failed chunk is retryable at the flow level rather than
resending the whole frame. Raise it to trade memory for fewer round-trips; lower
it for very wide rows.

Pass a `progress` callback to surface a running count, handy for a notebook bar
or a log line on a long load. It's called with the cumulative row count after
each chunk:

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
repeatedly: it lives server-side, so the client sends only its id, and the
server can optimise a known query. Reach for an ad-hoc `pipeline=` when the
shape is one-off or computed at runtime.

## Rules of thumb

- Default `batch_size` / `chunk_rows` are fine until profiling says otherwise;
  don't tune preemptively.
- Memory-bound? Stream (`iter_batches`) rather than raising `batch_size`.
- Throughput-bound on a bulk load? Raise `chunk_rows` so there are fewer chunks.
- A read that can't finish inside the deadline needs streaming, not just a
  bigger `timeout=`. See [Errors & retries](errors-and-retries.md#per-call-deadlines).
