# Worked example: export every actionflow script

A complete, end-to-end program against a **live** cluster: connect, page through
every actionflow task, and write each task's `script` to a file — a real
exercise of DNS discovery, auto-pagination, the generated `actionflow_task`
service, and typed errors, in one script.

!!! note "This example talks to a real cluster"
    Unlike the recipes elsewhere in these docs (which run against `LocalMock` in
    CI), this walkthrough reads live data — there's nothing to stub, the point
    is the round-trip against a real tenant. Paste your key, set your tenant,
    and run it top to bottom.

## Connect

With `cluster=None` the client resolves the CNAME of `{location}.clappform.com`
to pick the cluster, so tenant + key is all you need. `repr(cf)` confirms which
cluster you actually landed on.

```python
from pathlib import Path

from clappform import Clappform

LOCATION = "apps-dev"            # your tenant; the cluster is discovered from it
API_KEY = "PASTE_YOUR_KEY_HERE"  # ← your real API key
CLUSTER = None                   # None = discover; or "qa"/"qa-lts"/"prod"/""

cf = Clappform(location=LOCATION, cluster=CLUSTER, api_key=API_KEY)
cf   # Clappform(cluster='...', location='apps-dev', auth=ApiKey, version=..., protos=...)
```

## Pull every task and write its script to disk

`iter_get_all()` follows pagination for you — one loop, no page bookkeeping.
Each yielded `ActionflowTask` has a `script` field (bytes); give every task its
own file so the folder is ready to `grep`, diff, or analyse.

```python
import re

OUTPUT_DIR = "actionflow_scripts"
INCLUDE_DELETED = False
PAGE_LIMIT = 200


def slugify(name: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", name.strip()).strip("-")
    return slug.lower() or "unnamed"


out_dir = Path(OUTPUT_DIR)
out_dir.mkdir(parents=True, exist_ok=True)

rows, written, skipped_empty = [], 0, 0
seen_slugs: dict[str, int] = {}

for task in cf.client.actionflow_task.iter_get_all(
    limit=PAGE_LIMIT, include_deleted=INCLUDE_DELETED
):
    script_bytes = task.script or b""
    script_text = script_bytes.decode("utf-8", errors="replace")

    # Keep filenames unique even when two tasks share a name.
    base = slugify(task.name)
    seen_slugs[base] = seen_slugs.get(base, 0) + 1
    suffix = "" if seen_slugs[base] == 1 else f"-{seen_slugs[base]}"
    filename = f"{base}{suffix}.py"

    if script_bytes.strip():
        (out_dir / filename).write_text(script_text, encoding="utf-8")
        written += 1
    else:
        filename = None
        skipped_empty += 1

    rows.append(
        {
            "id": task.id,
            "name": task.name,
            "type": task.type,                     # "MODULE" / "TEMPLATE" / ""
            "n_actionflows": len(task.actionflows),
            "bytes": len(script_bytes),
            "file": filename,
            "updated_at": task.updated_at,
        }
    )

print(f"tasks seen:      {len(rows)}")
print(f"scripts written: {written}  -> {out_dir.resolve()}")
print(f"empty (skipped): {skipped_empty}")
```

## Analyse what came back

The summary rows drop straight into pandas, so you can spot patterns — script
sizes, the MODULE/TEMPLATE split, and tasks no actionflow references (cleanup
candidates).

```python
import pandas as pd

df = pd.DataFrame(rows).sort_values("bytes", ascending=False)
df.head(20)

# type breakdown
df.groupby("type").agg(
    tasks=("id", "count"),
    total_bytes=("bytes", "sum"),
)

# tasks not referenced by any actionflow — cleanup candidates
df[df["n_actionflows"] == 0][["name", "type", "bytes", "file"]]
```

## What this exercises

- **DNS-based cluster discovery** — `cluster=None` resolves the tenant's CNAME.
- **Auto-pagination** — `iter_get_all()` yields every task across all pages.
- **A generated Client-API service** — `cf.client.actionflow_task`, one of the
  many services on `cf.client` (see [Actionflows & listings](actionflows-and-listings.md)).
- **Typed errors** — any failure raises a `ClappformError` subclass carrying the
  cluster and tenant (see [Errors & retries](errors-and-retries.md)).

For the everyday building blocks this composes from, see the
[Cookbook](cookbook.md); for running code *inside* an actionflow worker rather
than driving one from outside, see [Actionflows](actionflow-scripts.md).
