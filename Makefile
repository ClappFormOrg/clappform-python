.PHONY: generate lint typecheck test check build clean

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

clean:
	rm -rf dist build src/clappform.egg-info .pytest_cache .mypy_cache .ruff_cache
