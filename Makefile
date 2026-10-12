.PHONY: generate lint typecheck test audit apicheck check build release-check clean docs docs-serve docs-test

generate:
	python tools/generate.py

lint:
	python -m ruff check .

typecheck:
	python -m mypy src/clappform tools

test:
	python -m pytest -q

# Resolve the installed tree against the PyPI and OSV advisory databases.
# --skip-editable drops the local editable clappform install, which has no
# published version to look up.
audit:
	python -m pip_audit --skip-editable --desc on

# Report public API removals and signature changes against the integration
# branch. Override the ref with `make apicheck AGAINST=v6.0.0a0`.
AGAINST ?= origin/Major/6
apicheck:
	python tools/apicheck.py --against $(AGAINST)

check: lint typecheck test

build:
	python -m build

# Build the distributions and validate their metadata, the same checks the
# Release workflow runs before the gated PyPI publish. Does not upload.
release-check: build
	python -m twine check dist/*

# Run the documented snippets against LocalMock, then build the site strictly
# (a broken include, dead reference or nav typo fails the build).
docs-test:
	python -m pytest -q tests/test_docs_snippets.py

docs: docs-test
	python -m mkdocs build --strict

docs-serve:
	python -m mkdocs serve

clean:
	rm -rf dist build site src/clappform.egg-info .pytest_cache .mypy_cache .ruff_cache
