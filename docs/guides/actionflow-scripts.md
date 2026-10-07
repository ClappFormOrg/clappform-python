# Running in an actionflow

Many scripts using this client don't run standalone; they run as tasks inside
an actionflow, on a worker that hands the task its location, a key, and its input
parameters. The client works the same way there as anywhere else; this guide
covers the two things specific to that context.

## Constructing the client in a worker

The library reads nothing from the environment: `location`, the cluster, and
the credential are always constructor arguments. So a task takes the values the
worker exposes and passes them in explicitly:

```python
--8<-- "actionflow_scripts.py:connect-in-worker"
```

That keeps the client honest about where its configuration comes from: there's
no hidden global state, no implicit env lookup, and the same code runs
identically on your laptop against a test tenant. Omitting `cluster=` discovers
it from the location's DNS record, which is usually what you want; pin it if the
worker runs somewhere discovery can't reach. Open the client once per task, in
the process that runs it, and close it when the task ends (see
[Client lifecycle](concepts.md#client-lifecycle)).

!!! note "Where the values come from is up to the worker"
    Different worker setups expose the location and key differently (task
    parameters, injected environment, a secrets helper). Whatever the source,
    the client's contract is the same: hand it a `location` and an `api_key`.

## Passing start parameters

When a task starts another actionflow, it often needs to hand it parameters:
a cursor, a date range, a batch id. Those ride on `custom_keys`, which today
takes JSON bytes, so build them from a plain dict and encode once:

```python
--8<-- "actionflow_scripts.py:start-params"
```

The response carries the run's `uuid`, so a task can start a flow and record or
return the id it kicked off.

## Everything else is the ordinary loop

Nothing about running in a worker changes how you read and write data. It's
the same DataFrame surface as the [Quickstart](../quickstart.md) and
[Cookbook](cookbook.md). A task can run again after a failure or a manual
re-run, so prefer writes that are safe to repeat, such as `upsert(on=...)`,
over `append()`:

```python
--8<-- "actionflow_scripts.py:read-write"
```

See [Actionflows & listings](actionflows-and-listings.md) for listing and
inspecting flows and their tasks, and [Error handling & retries](errors-and-retries.md)
for turning failures into the typed exceptions a task can branch on.
