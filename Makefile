.PHONY: generate lint typecheck test check build clean docs docs-serve docs-test

generate:
	python tools/generate.py

lint:
	python -m ruff check .

typecheck:
	python -m mypy src/clappform tools

test:
	python -m pytest -q

check: lint typecheck test

build:
	python -m build

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
