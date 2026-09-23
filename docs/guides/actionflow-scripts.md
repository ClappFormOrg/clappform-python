# Writing actionflow tasks

Many scripts using this client don't run standalone; they run as tasks inside
an actionflow, on a worker that hands the task its tenant, a key, and its input
parameters. The client works the same way there as anywhere else. This guide
covers what is specific to that context: constructing the client, the shape of
a task notebook, handing data from one task to the next, and starting other
flows.

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
it from the tenant's DNS record, which is usually what you want; pin it if the
worker runs somewhere discovery can't reach.

!!! note "Where the values come from is up to the worker"
    Different worker setups expose the tenant and key differently (task
    parameters, injected environment, a secrets helper). Whatever the source,
    the client's contract is the same: hand it a `location` and an `api_key`.

## The shape of a task

A task that is easy to configure, reuse and debug has the same parts, in order:

1. a cell that pins the libraries it imports,
2. a `parameters`-tagged cell declaring every input,
3. setup: logging and the client,
4. validation of every input,
5. the work, one operation,
6. an `output`-tagged cell binding what the next task needs.

The sections below take each in turn.

### Pin what you import

```python
%pip install -q 'clappform>=6.0.0a0,<7.0'
```

The upper bound keeps a new major release from changing the task between two
runs of the same flow. While 6.x is in pre-release the lower bound must name a
pre-release (`6.0.0a0`): pip skips pre-releases unless the specifier names one.

### Declare the parameters

One cell, tagged `parameters`, holds every input with its default. The runner
replaces the defaults with the values configured on the task, and the `# meta:`
JSON on each line builds the task's input form:

```python
--8<-- "actionflow_tasks.py:parameters"
```

| `meta` key | Effect |
|---|---|
| `description` | Help text next to the field. |
| `enum` | The allowed values; the form shows a dropdown. |
| `secret` | Marks a credential, supplied encrypted. |

**Annotate scalars, not the rest.** An annotation makes the service type-check
the configured value. Keep it on `str`, `int` and `bool` inputs, and leave it off
any input whose runtime value is a DataFrame, dict or list, such as `INPUT_DF`
above. An annotated `INPUT_DF: str` fails the check when a DataFrame arrives.

**Credentials are parameters.** Every key, token and password is a `secret`
parameter with an empty default, never a literal in the source. See
[Security & credentials](security.md).

### Set up

```python
--8<-- "actionflow_tasks.py:setup"
```

Log through a named logger rather than `print()`. The run log is where the next
person looks when a flow misbehaves, and `LOG_LEVEL` lets them turn up the
detail without editing the task.

### Validate

Check every input before any work, and raise `ValueError` with a message that
names the parameter. A failed run then says what to fix in the configuration.

Accept the forms a person is likely to type. A pipeline configured as a
parameter may arrive as a JSON string, an empty string, or an already-parsed
list; normalise all three to one shape:

```python
--8<-- "actionflow_tasks.py:read-validate"
```

### Do the work

Keep the work to the one operation the task exists for. A task that does two
unrelated things is better as two tasks, so each can be reused and rerun on its
own.

```python
--8<-- "actionflow_tasks.py:read-work"
```

### Expose the output

The last cell, tagged `output`, binds one variable. The runner stores it for
the next task:

```python
--8<-- "actionflow_tasks.py:read-output"
```

Name it after what it holds (`aggregated_df`, `excel_path`), because the next
task refers to it by that name in its own configuration. When the output is a
file, output its local path rather than its bytes; see
[Files, Excel & storage](files-and-storage.md).

## Handing data between tasks

A downstream task takes the upstream output's **name** as a parameter, and
reads the value from the notebook globals the runner injects. Check the type
before using it, so a misspelled name fails with a clear message:

```python
--8<-- "actionflow_tasks.py:transform"
```

```python
--8<-- "actionflow_tasks.py:transform-output"
```

The transform needs no client and no credentials: it works only on the
DataFrame it was handed, which also makes it the easiest task to test. Bind a
sample DataFrame to `aggregated_df` in a local notebook and run the cells.

## A write whose mode is a parameter

A task that stores its input often needs to insert on one flow and upsert on
another. Map a `MODE` parameter onto the collection handle's write methods:

```python
--8<-- "actionflow_tasks.py:write-mode"
```

| Mode | Call | Matches on |
|---|---|---|
| `insert` | `append(df)` | nothing: every row is a new document |
| `update` | `update(df)` | `_id` |
| `upsert` | `upsert(df, on=ON_KEY)` | the business column `ON_KEY` |
| `delete` | `delete(oids=...)` | `_id` |

!!! warning "`update` and `delete` need `_id`"
    `update()` sends rows by object id, and `delete(oids=...)` takes object
    ids, so both need the `_id` column that `read()` keeps. Passing a business
    column to either doesn't make it match on that column. To match on a
    business key, use `upsert(df, on=...)`.

For a flow that runs on a schedule, `upsert` on a stable business key is the
safe default: `insert` adds a second copy of every row on the second run, while
`upsert` updates the rows that exist and inserts the rest. An empty input
writes nothing and still succeeds, so a quiet day doesn't fail the flow.

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
[Cookbook](cookbook.md):

```python
--8<-- "actionflow_scripts.py:read-write"
```

See [Files, Excel & storage](files-and-storage.md) for tasks that export to or
load from files, [Actionflows & listings](actionflows-and-listings.md) for
listing and inspecting flows and their tasks, and
[Error handling & retries](errors-and-retries.md) for turning failures into the
typed exceptions a task can branch on.
