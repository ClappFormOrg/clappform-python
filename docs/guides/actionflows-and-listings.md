# Actionflows & listings

The [DataFrame flows](dataframes.md) cover reading and writing a collection's
rows. The operations here live on `cf.client` instead: starting an actionflow,
and listing the objects in a location: collections, apps, saved queries and
cronjobs. They're the everyday non-data-plane calls.

## How listings page

A listing RPC takes a page request and returns one page plus a `pagination`
message (`page`, `limit`, `total`, `pages`). The client generates two methods
for each:

- **The plain call** (`get_all()` on `cf.client`, `read_all()` on most of
  `cf.auth`) returns one page: the whole response message, with every list it
  carries and its `pagination`. `limit` is the page size and `page` picks the
  page.
- **The `iter_` twin** (`iter_get_all()`, `iter_read_all()`) yields the items
  across every page. It requests page 1, 2, 3 and so on, and stops at the first
  empty page or once it has fetched `pagination.pages` pages. It takes the same
  arguments except `page`, so `limit` sets how many items each request fetches.

When a response carries more than one list, the `iter_` twin yields only the
first; call the plain method for the others. `cf.client.actionflow.get_all()`
returns `actionflows` and `actionflow_tasks`, and `iter_get_all()` yields only
the actionflows. The method's docstring in the
[API families reference](../reference/api-families.md) names the list it
yields.

## Start an actionflow

Trigger an actionflow by id. The response carries the run's `uuid`, so you can
correlate the run with the tasks it spawns or surface it to a caller. Pass
`user_id=` to attribute the run, or `custom_keys=` (JSON bytes) to hand it
start parameters. See
[Passing start parameters](actionflow-scripts.md#passing-start-parameters) for
how to build them from a dict.

```python
--8<-- "client_operations.py:start-actionflow"
```

## List actionflows

`iter_get_all()` yields every actionflow across all pages, so you never manage
`page` yourself. When you want the pagination metadata, the first page only, or
the response's other lists, call `get_all()` directly.

```python
--8<-- "client_operations.py:list-actionflows"
```

`cf.client.actionflow_task` mirrors this exactly (`get_all()` / `iter_get_all()`
/ `get(id=...)`) for the tasks an actionflow is composed of.

## Read all collections

Listing collections is how you discover what's there to read. Each `Collection`
carries its `slug` and `id`, the same id `cf.data.collection(slug)` resolves to
internally, so this is the bridge from "what collections exist" to the
DataFrame flows.

```python
--8<-- "client_operations.py:list-collections"
```

## List apps, saved queries and cronjobs

The same `get_all()` / `iter_get_all()` pair lists the rest of the location's
objects. Anything on `cf.client` with a listing follows this shape.

```python
--8<-- "client_operations.py:list-others"
```

## Listings on `cf.auth`

The authoriser names its listings `read_all()` / `iter_read_all()` (API keys,
users, roles, security profiles and `cf.auth.azure`); only `cf.auth.version` uses
`get_all()`. They page the same way.

```python
--8<-- "client_operations.py:list-auth"
```

## Everything else on `cf.client`

`cf.client` wraps one method per RPC across the whole client API. Beyond the
listings above it also carries `page`, `widget`, `group`, `row`, `collection_rule`,
`process`, `secret` and more, each with the same `get_all` / `get` / `create` /
`update` / `delete` surface where the RPC exists. Cronjobs additionally expose
`start(id=...)` / `stop(id=...)` (and `start_all()` / `stop_all()`); `transfer`
moves a whole app between instances (see
[Moving a whole app between instances](multi-cluster.md#moving-a-whole-app-between-instances)).
The [API families reference](../reference/api-families.md) is the generated,
exhaustive list.

!!! note "Stubbing these in your own tests"
    None of these are data-plane RPCs, so
    [`LocalMock`][clappform.testing.LocalMock] has no built-in handler for
    them. The snippets above back each with an explicit
    `.on(method_path, response)` stub.
    That's the same pattern you use to test your own code that calls them; see
    [Testing with LocalMock](testing.md#stub-any-other-rpc).
