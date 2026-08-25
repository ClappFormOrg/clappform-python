# Key concepts & glossary

The rest of the docs assume these terms. If you already work with Clappform,
most will be familiar — this page pins down the few that are easy to conflate
(especially **location vs cluster** and **query vs pipeline**).

## The client binding

A `Clappform` instance is one binding of three things:

- **`location`** — your **tenant**: a client subdomain (e.g. `acme`), sent as
  metadata on *every* call. It selects which tenant database the server uses.
- **`cluster`** — the set of **hosts** that serve that tenant (e.g. `prod`,
  `qa`, `qa-lts`, or `""` for the main cluster). It selects *where* calls go.
- **credential** — an API key (the only credential this line ships).

!!! important "`location` ≠ `cluster`"
    They are independent axes. `location` picks the tenant; `cluster` picks the
    hosts. Two tenants can live on the **same** cluster, and the same tenant
    name could exist on different clusters. When you omit `cluster`, it's
    discovered from the tenant's DNS record — but the `location` header is
    always sent regardless. `repr(cf)` shows both.

Nothing is global: two `Clappform` instances (two clusters, or two tenants)
coexist in one process without interfering. See
[Multi-cluster & multi-tenant](multi-cluster.md).

## Data entities

- **Collection** — a store of JSON documents (rows), each with an `_id`. The
  DataFrame surface (`cf.data.collection(ref)`) reads and writes these. Backed by
  Mongo or Elastic; the server picks the backend from the collection's settings.
- **Document / row / record** — one JSON object in a collection. `read()` keeps
  its `_id` as a column so a read → mutate → `update()` round-trip works.
- **Saved query** — a **prewritten aggregation stored server-side** that already
  knows its own collection and pipeline. You read it by name/UUID
  (`cf.data.query(ref)`) without writing any pipeline client-side.

!!! important "“Query” means the saved entity — not a filter"
    In Clappform vocabulary a *Query* is the saved server-side object above.
    That's why the client has **no `query=` filter argument**: a filtered read
    takes an aggregation `pipeline`, and the word "query" is reserved for the
    saved entity. See [Read & query data](dataframes.md).

- **Pipeline** — a list of aggregation stages (`$match`, `$project`, `$group`,
  `$sort`, …) you pass to `read(pipeline=...)` / `aggregate(...)`. The client
  sends it to the server **verbatim** — it doesn't interpret a query language of
  its own, so use the syntax the collection's backend expects.
- **Index** — a collection index, managed via `cf.data.index`
  (create/list/delete). See the [Cookbook](cookbook.md#manage-indexes).

## Identifiers

- **UUID** — the wire identifier for collections and saved queries.
- **Slug** — a human-readable name for the same entity. `collection(ref)` and
  `query(ref)` accept **either**: a string that parses as a UUID is used as-is;
  anything else is treated as a slug and resolved to its UUID once, then cached
  per tenant (so a slug costs one extra lookup per process, not per call).

## Platform entities

- **Actionflow** — an orchestrated flow you trigger by id
  (`cf.client.actionflow.start(id=...)`); the response carries the run's `uuid`.
- **Actionflow task** — a single script/step an actionflow is composed of,
  listed via `cf.client.actionflow_task`.
- **Cronjob** — a scheduled trigger; `cf.client.cronjob` (list, `start`/`stop`).
- **App** — a bundle of collections, queries, actionflows and questionnaires;
  movable between instances via `cf.client.transfer`
  (see [Move an app](cookbook.md#move-an-app-between-instances)).

## API families

Calls are grouped by the proto family they belong to:

- **`cf.data`** — the data plane (collections, aggregation, insert/update/delete,
  indexes, schema, exports, embeddings, rules, …). The DataFrame handles
  (`cf.data.collection` / `cf.data.query`) live here too.
- **`cf.client`** — the platform API (apps, collections metadata, actionflows,
  cronjobs, transfer, …).
- **`cf.auth`** — the authoriser (API keys, users, roles, …).
- **`cf.notifier`** — messaging: one-off sends (`cf.notifier.direct`), batches,
  the inbox, delivery policies, per-user preferences, frequency caps and
  channel connections.

The family segment disambiguates names that repeat across services (`get`,
`create`, `delete` exist on many). See the
[API families reference](../reference/api-families.md).

## Testing

- **`LocalMock`** — an in-process transport double. It serves the data-plane
  RPCs against a seeded store (running `$match`/`$project`/`$limit`, **not**
  `$group`) and lets you stub any other RPC with `.on()`. It's how every
  snippet in these docs runs in CI. See [Testing with LocalMock](testing.md).
