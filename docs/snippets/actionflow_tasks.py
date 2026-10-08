"""Runnable source for the "writing an actionflow task" guide snippets.

Covers the shape of a task notebook (a parameters cell, setup, validation, the
work, an output cell) and the patterns that recur in real tasks: a pipeline
supplied as JSON config, resolving an upstream task's output by name, and a
write whose mode is a parameter.

A task resolves an upstream task's output from the notebook globals the runner
injects. The snippets reproduce that by binding the upstream value as a module
global before the block that reads it. Runs against ``LocalMock`` in the
docs-test job.
"""

from __future__ import annotations

import json
import logging
from typing import Any

import pandas as pd

from clappform.testing import LocalMock

log = logging.getLogger("actionflow_tasks")


def build_mock() -> LocalMock:
    # include_unreleased=True emulates update(), which the Data Connector does
    # not serve yet; the guide marks the update mode with a warning.
    mock = LocalMock(include_unreleased=True)
    mock.seed_collection_slug("rental_units", id="rental_units-id")
    mock.seed(
        "rental_units-id",
        [
            {"unit_id": "U-1", "municipality": "Utrecht", "rent": 812.0, "status": "let"},
            {"unit_id": "U-2", "municipality": "Utrecht", "rent": 745.5, "status": "vacant"},
            {"unit_id": "U-3", "municipality": "Zeist", "rent": 690.0, "status": "let"},
            {"unit_id": "U-4", "municipality": "Utrecht", "rent": 901.0, "status": "let"},
        ],
    )
    mock.seed_collection_slug("unit_summary", id="unit_summary-id")
    mock.seed("unit_summary-id", [])
    return mock


def task_shape() -> Any:
    """The parameters and setup cells a task opens with."""
    from clappform import Clappform

    # --8<-- [start:parameters]
    # parameters-tagged cell: every input, with a `# meta:` annotation that
    # drives the platform's input form.
    LOG_LEVEL: str = "INFO"  # meta: {"enum": ["INFO", "DEBUG"], "description": "log level"}
    LOCATION: str = ""  # meta: {"description": "Location; the cluster is discovered from it"}
    API_KEY: str = ""  # meta: {"secret": true, "description": "Clappform API key"}
    COLLECTION: str = ""  # meta: {"description": "Collection id or slug"}
    # Upstream DataFrame: no annotation, so the service doesn't type-check it.
    INPUT_DF = ""  # meta: {"description": "Upstream output variable holding the DataFrame"}
    # --8<-- [end:parameters]

    # The runner replaces the defaults above with the configured values.
    LOCATION, API_KEY, COLLECTION = "acme", "cf_live_...", "rental_units"

    # --8<-- [start:setup]
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL, logging.INFO),
        format="%(name)s:%(levelname)s:%(message)s",
    )
    log = logging.getLogger("my_task")

    # cluster=None discovers the cluster from LOCATION's DNS record.
    cf = Clappform(location=LOCATION, cluster=None, api_key=API_KEY)
    # --8<-- [end:setup]

    log.info("connected: %s (%s, input=%r)", cf, COLLECTION, INPUT_DF)
    return cf


def read_from_config(cf: Any, COLLECTION: str, PIPELINE: Any) -> pd.DataFrame:
    """Read a collection through a pipeline that arrives as configuration."""
    BATCH_SIZE = 500

    # --8<-- [start:read-validate]
    collection = (COLLECTION or "").strip()
    if not collection:
        raise ValueError("COLLECTION is required")

    # Accept an empty pipeline, a JSON string, or an already-parsed list.
    raw_pipeline = PIPELINE if isinstance(PIPELINE, str) else json.dumps(PIPELINE)
    pipeline = json.loads(raw_pipeline) if raw_pipeline.strip() else []
    if not isinstance(pipeline, list):
        raise ValueError("PIPELINE must be a JSON array of stages")
    # --8<-- [end:read-validate]

    # --8<-- [start:read-work]
    handle = cf.data.collection(collection)
    if pipeline:
        df = handle.aggregate(pipeline, batch_size=BATCH_SIZE)
    else:
        df = handle.read(batch_size=BATCH_SIZE)
    log.info("read %d rows x %d columns", len(df), df.shape[1])
    # --8<-- [end:read-work]

    # --8<-- [start:read-output]
    aggregated_df = df
    # --8<-- [end:read-output]
    return aggregated_df


def transform_task() -> pd.DataFrame:
    """A task that consumes one task's output and produces the next one's input."""
    INPUT_DF = "aggregated_df"

    # --8<-- [start:transform]
    # Resolve the upstream DataFrame by the variable name in INPUT_DF.
    source = globals().get(INPUT_DF)
    if not isinstance(source, pd.DataFrame):
        raise ValueError(
            f"expected a DataFrame in upstream output {INPUT_DF!r}, "
            f"got {type(source).__name__}"
        )

    summary = (
        source.groupby("municipality", as_index=False)
        .agg(units=("unit_id", "count"), avg_rent=("rent", "mean"))
        .round({"avg_rent": 2})
    )
    # --8<-- [end:transform]

    # --8<-- [start:transform-output]
    summary_df = summary
    # --8<-- [end:transform-output]
    return summary_df


def write_in_mode(cf: Any, COLLECTION: str, MODE: str, df: pd.DataFrame, ON_KEY: str) -> int:
    """A write whose mode is a task parameter."""
    CHUNK_ROWS = 500

    # --8<-- [start:write-mode]
    MODES = ("insert", "update", "upsert", "delete")
    if MODE not in MODES:
        raise ValueError(f"MODE must be one of {MODES}, got {MODE!r}")
    # update and delete match on _id; upsert matches on a business column.
    key = ON_KEY if MODE == "upsert" else "_id"
    if MODE != "insert" and key not in df.columns:
        raise ValueError(f"{MODE} needs a {key!r} column in the input DataFrame")

    handle = cf.data.collection(COLLECTION)
    if df.empty:
        log.warning("input DataFrame is empty; nothing to %s", MODE)
        written = 0
    elif MODE == "insert":
        written = handle.append(df, chunk_rows=CHUNK_ROWS)
    elif MODE == "update":
        written = handle.update(df, chunk_rows=CHUNK_ROWS)
    elif MODE == "upsert":
        written = handle.upsert(df, on=key, chunk_rows=CHUNK_ROWS)
    else:
        oids = [str(v) for v in df["_id"].dropna()]
        if not oids:
            raise ValueError("delete found no ids in the _id column")
        handle.delete(oids=oids)
        written = len(oids)
    # --8<-- [end:write-mode]
    return written


def run(transport: LocalMock) -> None:
    from clappform import Clappform

    # Exercise the reader-facing setup block (discovery is stubbed in the test),
    # then run the tasks against the mock transport.
    task_shape().close()

    g = globals()
    cf = Clappform(location="acme", cluster="prod", api_key="cf_live_...", transport=transport)
    try:
        with cf:
            # Every accepted PIPELINE form: JSON string, parsed list, empty.
            let = read_from_config(cf, "rental_units", '[{"$match": {"status": "let"}}]')
            assert len(let) == 3
            assert len(read_from_config(cf, "rental_units", [{"$match": {"status": "let"}}])) == 3
            assert len(read_from_config(cf, "rental_units", "")) == 4

            # The runner stores each task's output and injects it, by name,
            # into the next task's globals.
            g["aggregated_df"] = let
            summary = transform_task()
            assert len(summary) == 2

            # upsert twice: the second run updates in place, no duplicates.
            assert write_in_mode(cf, "unit_summary", "upsert", summary, "municipality") == 2
            assert write_in_mode(cf, "unit_summary", "upsert", summary, "municipality") == 2
            assert len(transport.records("unit_summary-id")) == 2

            # update and delete round-trip through _id from a read.
            stored = cf.data.collection("unit_summary").read()
            stored["units"] = stored["units"] + 1
            assert write_in_mode(cf, "unit_summary", "update", stored, "") == 2
            assert write_in_mode(cf, "unit_summary", "delete", stored.head(1), "") == 1
            assert len(transport.records("unit_summary-id")) == 1
    finally:
        g.pop("aggregated_df", None)


if __name__ == "__main__":
    from clappform import _discovery

    _discovery.discover_cluster = lambda location: "prod"
    run(build_mock())
