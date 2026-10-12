# Key concepts & glossary

The rest of the docs assume these terms. If you already work with Clappform,
most will be familiar. This page pins down the few that are easy to conflate
(especially **location vs cluster** and **query vs pipeline**) and how a
client's lifetime works.

## The client binding

A `Clappform` instance is one binding of three things:

- **`location`** is the client environment, the **tenant**: a subdomain such
  as `acme` in `acme.clappform.com`, sent as metadata on *every* call. It
  selects which tenant database the server uses. These docs say "location"
  throughout.
- **`cluster`** is the set of **hosts** that serve that location. It is a host
  extension: `""` for the main cluster, or another cluster's extension such as
  `"qa"` or `"prod-lts"`. `"prod"` is accepted as another name for the main
  cluster `""`; it is not `"prod-lts"`. It selects *where* calls go.
- **credential** is an API key (the only credential this line ships).

!!! important "`location` ≠ `cluster`"
    They are independent axes. `location` picks the tenant; `cluster` picks the
    hosts. Two locations can live on the **same** cluster. When you omit
    `cluster`, it's discovered from the DNS record of
    `{location}.clappform.com`, but the `location` header is always sent
    regardless. `repr(cf)` shows both. Passing `transport=` (such as
    `LocalMock`) skips discovery, and `cf.cluster` is then `None` unless you
    name one.

Nothing is global: two `Clappform` instances (two clusters, or two locations)
coexist in one process without interfering. See
[Multi-cluster & multi-tenant](multi-cluster.md).

## Client lifecycle

A client opens one gRPC channel per host the first time it calls that API
family, and keeps it open until you close the client. Use it as a context
manager, or call `close()` yourself:

```python
--8<-- "lifecycle.py:close"
```

A closed client stays closed. Any call on it raises
[`ConfigurationError`][clappform.ConfigurationError] with "client is closed"
before anything reaches the network:

```python
--8<-- "lifecycle.py:closed"
```

**Clones from `with_location()`** follow who owns the connections:

- A clone on the same cluster shares the parent's channels. Closing the clone
  does nothing, and closing the parent breaks every clone that shares them.
- A clone whose location the client re-discovered onto a **different** cluster
  gets its own channels, and you must close it. Use it as a context manager.
- `with_location()` with the client's own location returns the client itself,
  so a `with` block around it closes the original.

```python
--8<-- "lifecycle.py:clones"
```

```python
--8<-- "lifecycle.py:rediscovered"
```

A client you build with `transport=` never closes that transport; closing it is
up to you.

**Threads.** A client is safe to share across threads: channels are created
under a lock, and gRPC channels are thread-safe. Share one client rather than
building one per thread. `LocalMock` is not thread-safe.

**Processes.** gRPC does not survive `fork()`. Create clients in the process
that uses them, after any `fork` (including `multiprocessing` workers started
with the `fork` method), never before.

## Data entities

- **Collection** is a store of JSON documents (rows), each with an `_id`. The
  DataFrame surface (`cf.data.collection(ref)`) reads and writes these. Backed by
  Mongo or Elastic; the server picks the backend from the collection's settings.
- **Document / row / record** is one JSON object in a collection. `read()` keeps
  its `_id` as a column so a frame can be matched back to its documents.
- **Saved query** is a **prewritten aggregation stored server-side** that already
  knows its own collection and pipeline. You read it by **name** or UUID
  (`cf.data.query(ref)`) without writing any pipeline client-side.

!!! important "“Query” means the saved entity, not a filter"
    In Clappform vocabulary a *Query* is the saved server-side object above.
    That's why the client has **no `query=` filter argument**: a filtered read
    takes an aggregation `pipeline`, and the word "query" is reserved for the
    saved entity. See [DataFrame flows](dataframes.md).

- **Pipeline** is a list of aggregation stages (`$match`, `$project`, `$group`,
  `$sort`, …) you pass to `read(pipeline=...)` / `aggregate(...)`. The client
  has no query language of its own: it encodes the stages as JSON, converting
  Python values as described in [Type mapping](dataframes.md#type-mapping), and
  the server runs them. Use the syntax the collection's backend expects.
- **Index** is a collection index, managed via `cf.data.index`
  (create/list/delete). See the [Cookbook](cookbook.md#manage-indexes).

## Identifiers

- **UUID** is the wire identifier for collections and saved queries.
- **Slug** is a collection's human-readable identifier; a saved query's is its
  **name**. `collection(ref)` takes a slug or a UUID, and `query(ref)` takes a
  name or a UUID. A string that parses as a UUID is used as-is.
- **Resolution.** Anything else is resolved through the Client API: the
  client lists every collection (or saved query) in the location, page by page,
  until one's `slug` (or `name`) matches. The result is cached per location on
  the client and its `with_location()` clones, so the scan runs once per
  identifier, not per call. A cached id that later answers `NOT_FOUND` is
  resolved again once. An identifier that matches nothing raises
  `NotFoundError` naming it and the location searched.

## Platform entities

- **Actionflow** is an orchestrated flow you trigger by id
  (`cf.client.actionflow.start(id=...)`); the response carries the run's `uuid`.
- **Actionflow task** is a single script or step an actionflow is composed of,
  listed via `cf.client.actionflow_task`.
- **Cronjob** is a scheduled trigger; `cf.client.cronjob` (list, `start`/`stop`).
- **App** is a bundle of collections, queries, actionflows and questionnaires;
  movable between instances via `cf.client.transfer`
  (see [Move an app](cookbook.md#move-an-app-between-instances)).

## API families

Calls are grouped by the proto family they belong to:

- **`cf.data`** is the data plane (collections, aggregation, insert/update/delete,
  indexes, schema, exports, embeddings, rules, …). The DataFrame handles
  (`cf.data.collection` / `cf.data.query`) live here too.
- **`cf.client`** is the platform API (apps, collections metadata, actionflows,
  cronjobs, transfer, …).
- **`cf.auth`** is the authoriser (API keys, users, roles, …).
- **`cf.notifier`** handles messaging: one-off sends (`cf.notifier.direct`),
  batches, the inbox, delivery policies, per-user preferences, frequency caps
  and channel connections.

The family segment disambiguates names that repeat across services (`get`,
`create`, `delete` exist on many). See the
[API families reference](../reference/api-families.md).

## Testing

- **`LocalMock`** is an in-process transport double. It serves the data-plane
  RPCs against a seeded store (running `$match`, `$project`, `$sort`, `$skip`
  and `$limit`, and raising on any other stage) and lets you stub any other RPC
  with `.on()`. It's how every snippet in these docs runs in CI. See
  [Testing with LocalMock](testing.md).
