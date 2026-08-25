# Changelog

The client pins the `commons` proto repo by git tag, so every release records
the proto version it was generated against — a client's behaviour is a function
of both its own version and the protos it wraps. `clappform.__proto_version__`
reports the pinned proto tag at runtime, and `repr(client)` includes it.

!!! note "Per-release entries"
    Release entries — including each release's proto diff — are published from
    the release workflow that also pushes to PyPI, so this page fills in as
    versions ship. The versions below track the 6.x line; the 4.x HTTP-era docs
    remain archived under their own version tag.

## 6.0.0 (alpha)

### Proto pin: `commons` v1.6.2 → v1.7.2

The generated surface is regenerated from `commons` v1.7.2. Anyone already on
`6.0.0a0` should read this section before upgrading.

**Removed RPCs.** The notifier and chat protos were reorganised upstream, and
these methods no longer exist:

| Removed | Replacement |
| --- | --- |
| `cf.notifier.outbound.send_message` (whole service) | `cf.notifier.direct.send_email` / `send_push` / `send_slack` / `send_teams`, or `cf.notifier.batch.send_batch` |
| `cf.notifier.whatsapp.send_message` / `send_template` | `cf.notifier.direct.send_whats_app_message` / `send_whats_app_template` |
| `cf.notifier.inbox.get_messages` / `stream_messages` | `cf.notifier.inbox.get_notifications` |
| `cf.notifier.inbox.set_status` | `cf.notifier.inbox.mark_as_read` / `mark_as_acknowledged` / `bulk_update_status` |
| `cf.notifier.inbox.send_message` | `cf.notifier.direct.*` or `cf.notifier.policy.send_from_policy` |
| `cf.data.chat.get_rooms` / `update_room` / `delete_room` | `cf.data.chat.get_chats` / `update_chat` / `delete_chat` (plus `create_chat` / `get_chat`) |
| `cf.data.chat.stream_message` | `cf.data.chat.send_message` |
| `cf.data.chat.upload_files` / `delete_file` | `cf.data.embeddings` — `create` returns a write-only SAS URL, the client PUTs the bytes to it, then `finalize` runs the chunk/embed pipeline |

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
- First-class pandas DataFrame flows (`read` / `append` / `update` / `upsert` /
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
