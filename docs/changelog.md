# Changelog

The client pins the `commons` proto repo by git tag, so every release records
the proto version it was generated against, because a client's behaviour is a
function of both its own version and the protos it wraps. `clappform.__proto_version__`
reports the pinned proto tag at runtime, and `repr(client)` includes it.

!!! note "Per-release entries"
    Each release's notes, including its proto diff, go in the GitHub Release
    body; step 3 of [RELEASING.md](https://github.com/ClappFormOrg/clappform-python/blob/main/RELEASING.md)
    covers that. Add the same entry to this page in the release commit. The
    versions below track the 6.x line; the 4.x HTTP-era docs remain archived
    under their own version tag.

## 6.0.0a2 (unreleased)

### Breaking changes

- `CollectionHandle.replace_where()` is renamed to `update_where()`, since it
  sets fields rather than replacing documents. `replace_where()` still works,
  emits a `DeprecationWarning`, and is removed before 6.0.0. `update_where({})`
  raises `ValueError`.
- `append()` raises `ValueError` for a frame with an `_id` column, because the
  server rejects inserts that carry one. Drop the column first.
- `upsert()` raises `ValueError` for a frame with an `_id` column. The server
  writes the row's `_id` into the replacement document, and the string `_id`
  that `read()` returns does not equal the stored ObjectId. `LocalMock` rejects
  a `SyncManyByField` row whose `_id` differs from the matched document's.
- `append()`, `update()` and `upsert()` raise `ValueError` for a frame with a
  named index, such as one from `set_index()` or `groupby()`, instead of
  dropping it. Call `df.reset_index()` first.
- Only RPCs named for a read (`Get*`, `List*`, `Read*`, `Describe*`,
  `Aggregate*`, `Download*`, `Health`, `Preview*`) retry `UNAVAILABLE`.
  Actions such as `actionflow.start` and `transfer.import_app`, and every
  other write, no longer retry. `clappform._transport.NON_RETRIED_SERVICES` is
  removed.
- Streaming calls, which include every DataFrame read and write, have no
  deadline by default. `timeout=` (default 60 s) now applies to unary calls
  only; the new `stream_timeout=` (default `None`) applies to streams. A
  per-call `timeout=` bounds that whole call, stream included.
- `ReadResult.__arrow_c_stream__` is removed. Polars, DuckDB and pyarrow probe
  for it and would call a stub that could only raise. `to_arrow()` and
  `to_polars()` still raise `NotImplementedError`.
- `grpcio>=1.68` is required: the generated stubs raise `RuntimeError` at
  import on an older grpcio.
- `RetryPolicy` takes backoffs in seconds as floats (`"0.2s"` strings still
  work) and validates its fields: `max_attempts` must be 2 to 5, since gRPC
  caps it at 5, and backoffs and the multiplier must be positive. Invalid values
  raise `ConfigurationError`.
- `LocalMock` raises `NotSupportedError` for `UpdateMany`, `UpdateManyByField`,
  `UpdateManyByQuery` and `DeleteManyByQuery`, as the Data Connector does,
  unless built with `LocalMock(include_unreleased=True)`. It rejects inserts
  that carry `_id`.
- `LocalMock`'s pipeline emulation raises `ClappformError` for any stage other
  than `$match`, `$project`, `$sort`, `$skip` and `$limit`, and for any
  `$match` operator other than `$eq`, `$ne`, `$gt`, `$gte`, `$lt`, `$lte`,
  `$in`, `$nin` and `$exists`, instead of passing the rows through. Stub
  `AggregateStream` with `.on()` for other pipelines.

### Not served yet

`update()`, `update_where()` and `delete(where=...)` call RPCs the Data
Connector does not implement yet, so they raise `NotSupportedError` on every
cluster. Use `upsert(on=...)`, `delete(oids=...)` and `clear()`.

### Writes and retries

- Writes and actions are never retried, because a retried `UNAVAILABLE`
  call can apply twice. Reads still retry `UNAVAILABLE`.
- `append()` reports progress, and returns, the rows the server acknowledged.
  When it fails, the raised `ClappformError` carries `rows_written`.
- `update(df, on=...)` sends `UpdateMany` for `on="_id"` and
  `UpdateManyByField` for any other column, setting the frame's columns and
  leaving other fields alone. A row with a null or NaN key raises `ValueError`.
- `delete(oids=[])` makes no call.
- New `ResourceExhaustedError` for `RESOURCE_EXHAUSTED`, such as a message
  over the 64 MiB gRPC limit. It was a plain `ClappformError` before.
- `TransientError` still covers `UNAVAILABLE` and `DEADLINE_EXCEEDED`;
  `DEADLINE_EXCEEDED` is never retried.

### Client and streams

- Passing `transport=` skips DNS discovery; `cf.cluster` is then `None` unless
  you pass `cluster=`.
- DNS discovery gives up after 5 seconds and raises `ConfigurationError`
  telling you to pass `cluster=`.
- A response stream you stop reading is cancelled on the server.
- An exception raised while the client produces a request stream, such as one
  from a `progress` callback or a bad item, reaches the caller instead of
  surfacing as a cancelled call.

### Codec

numpy scalars and arrays, `Decimal` (as a float), `UUID` (as a string) and sets
now encode. Any other value JSON cannot hold raises `TypeError` naming its type.

### Generated methods

Generated methods take a request message or field keyword arguments. Setting
two members of one `oneof` raises `TypeError` instead of keeping the last.

### LocalMock

`$match` supports equality and `$eq`, `$ne`, `$gt`, `$gte`, `$lt`, `$lte`,
`$in`, `$nin` and `$exists` on top-level fields, alongside `$project`, `$sort`,
`$skip` and `$limit`. The [testing guide](guides/testing.md) now covers
`seed_collection_slug()`, `seed_query()`, `records()`, `reset()`,
`include_unreleased` and stubs that raise.

### Generated method names and arguments

Changes since `6.0.0a1` to how the service layer names things:

| Before | After |
| --- | --- |
| `cf.auth.azure.azure_auth_o_auth_acs` | `cf.auth.azure.azure_auth_oauth_acs` |
| `cf.auth.azure.azure_auth_samlacs` | `cf.auth.azure.azure_auth_saml_acs` |
| `cf.notifier.direct.send_whats_app_message` | `cf.notifier.direct.send_whatsapp_message` |
| `cf.notifier.direct.send_whats_app_template` | `cf.notifier.direct.send_whatsapp_template` |

A request field named `timeout`, `metadata`, `location`, `request`, `requests`
or `self`, or named after a Python keyword such as `from`, is now a keyword
argument with a trailing underscore. `cf.client.actionflow_task.create(timeout_=300)`
sets the task's `timeout` field, while `timeout=` stays the gRPC deadline.
Before, those fields could only be set through a prebuilt request message.

`iter_*` methods request page 1, 2, 3 and so on, and stop at the first empty
page or once the requested page reaches `pagination.pages`, so a server that
echoes `page=0` or ignores the requested page no longer loops forever.

### Documentation

The `Clappform` constructor documents every argument in the
[Client reference](reference/client.md), and the generated per-RPC reference is
split into one page per API family.

## 6.0.0 (alpha)

### Dependencies

The `protobuf` requirement moves from `>=4.25,<6` to `>=5.28.1,<8`. The floor is
a correction: `clappform/gen` carries gencode 5.28.1, and protobuf 4.x has no
`google.protobuf.runtime_version` while 5.27 and below fail protobuf's own
gencode-newer-than-runtime check, so `6.0.0a0` never imported on either. The
ceiling moves because every `grpcio-tools` release carrying a CPython 3.14 wheel
requires protobuf 6.31 or newer.

### Proto pin: `commons` v1.6.2 → v1.7.2

The generated surface is regenerated from `commons` v1.7.2. Anyone already on
`6.0.0a0` should read this section before upgrading.

**Removed RPCs.** The notifier and chat protos were reorganised upstream, and
these methods no longer exist:

| Removed | Replacement |
| --- | --- |
| `cf.notifier.outbound.send_message` (whole service) | `cf.notifier.direct.send_email` / `send_push` / `send_slack` / `send_teams`, or `cf.notifier.batch.send_batch` |
| `cf.notifier.whatsapp.send_message` / `send_template` | `cf.notifier.direct.send_whatsapp_message` / `send_whatsapp_template` |
| `cf.notifier.inbox.get_messages` / `stream_messages` | `cf.notifier.inbox.get_notifications` |
| `cf.notifier.inbox.set_status` | `cf.notifier.inbox.mark_as_read` / `mark_as_acknowledged` / `bulk_update_status` |
| `cf.notifier.inbox.send_message` | `cf.notifier.direct.*` or `cf.notifier.policy.send_from_policy` |
| `cf.data.chat.get_rooms` / `update_room` / `delete_room` | `cf.data.chat.get_chats` / `update_chat` / `delete_chat` (plus `create_chat` / `get_chat`) |
| `cf.data.chat.stream_message` | `cf.data.chat.send_message` |
| `cf.data.chat.upload_files` / `delete_file` | `cf.data.embeddings`: `create` returns a write-only SAS URL, the client PUTs the bytes to it, then `finalize` runs the chunk/embed pipeline |

`cf.notifier.whatsapp` keeps its webhook RPCs. `cf.data.chat.get_messages` drops
its `app_id` argument.

**`AggregateResponse.stats`.** Every aggregate response now carries a
`QueryExecutionStats` message (`duration_ms`, `docs_examined`, `docs_returned`,
`cache_hit`, `index_used`, `database_type`, `source_query_depth`,
`executed_at`). It replaces the raw explain blob that `explain=True` used to
write into `data`, so that flag no longer changes the shape of `data`. The
DataFrame surface is unaffected.

**New services.** `cf.data` gains `schema`, `usage`, `model`, `export`,
`embeddings`, `rule` and `query_eval`; `cf.notifier` gains `direct`, `batch`,
`policy`, `preference`, `freq_cap` and `connection`; `cf.auth.user` gains
`regenerate_recovery_codes`. `cf.auth.user.create` / `update` take
`preferences`, `cf.client.audit.get_all` takes `url` / `url_prefix`, and
`cf.data.process.execute_process` takes `response` / `outputs`.

### The rewrite

The greenfield rewrite. One package covering every Clappform gRPC API,
generated from the `commons` protos, with:

- A single `Clappform` client, one binding per `(cluster, location,
  credentials)`, with namespaced sub-clients (`data`, `client`, `auth`,
  `notifier`).
- pandas DataFrame flows (`read` / `append` / `update` / `upsert` /
  `replace_where` / `delete`) and saved-query reads. Reads take an aggregation
  `pipeline` (or none, for the whole collection); the client sends it verbatim
  and never interprets a query language of its own. `aggregate(p)` is the
  DataFrame-returning twin of `read(pipeline=p)`.
- Native multi-cluster / multi-tenant support with optional DNS-based cluster
  discovery.
- A typed error hierarchy that never leaks `grpc` to the caller.
- `LocalMock`, an in-process transport double for testing without
  infrastructure.

Configuration is constructor-only (no config files, no environment lookup) and
API-key auth is the only credential shipped in this line. Async, JWT/SSO auth,
the `nbflow` API, and Arrow/Polars output surfaces are designed-for but not yet
shipped.
