.PHONY: help install sync build format lint check mypy ruff clean

help: ## Display this help screen
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install all dependencies including dev dependencies
	@uv sync --all-groups

sync: install ## Alias for install

build: ## Build the package
	@uv build

format: ## Format source files with ruff
	@uv run ruff format clappform
	@uv run ruff check --fix clappform

mypy: ## Run mypy type checker
	@uv run mypy clappform

ruff: ## Check code with ruff (no fixes)
	@uv run ruff check --no-fix clappform
	@uv run ruff format --check clappform

check: mypy ruff ## Run all checks (mypy + ruff)

lint: check ## Alias for check

clean: ## Delete all temporary files
	@find clappform -type f -name '*.py[cod]' -delete
	@find clappform -type d -name '__pycache__' -delete
	@rm -rf *.egg *.egg-info build dist public .mypy_cache .ruff_cache
