# Clappform

Python client for the Clappform gRPC APIs. Version 6 is a ground-up rewrite:
the full API surface is generated from the shared proto definitions, with a
hand-written ergonomic layer for DataFrame workflows, multi-cluster
configuration, and typed errors.

> **Status: under active development on the `Major/6` branch.** The published
> 4.x/5.x packages are unrelated to this codebase.

## Install

```bash
pip install clappform[pandas]
```

Core dependencies are `grpcio` and `protobuf` only; `pandas`, `polars`, and
`pyarrow` are optional extras.

## Development

```bash
pip install -e .[dev,pandas]
make generate   # regenerate clappform/gen and clappform/services from protos
make check      # ruff + mypy + pytest
```

Code generation reads the proto definitions from the commons repository at
the tag pinned in `COMMONS_VERSION`. Point `CLAPPFORM_COMMONS_DIR` at a local
clone of commons (defaults to a sibling `../commons` checkout).

Generated code under `src/clappform/gen/` and `src/clappform/services/` is
committed; do not edit it by hand.
