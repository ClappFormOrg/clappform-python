.PHONY: all help install required build release black mypy pylint flake8 ruff lint docker clean

all: install required clean

help: ## Display this help screen
	@grep -E '^[a-zA-Z0-9_]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "%-15s %s\n", $$1, $$2}'

install: ## Install a dependencies for development
	@pip install -r requirements-dev.txt --upgrade

required: ## Install requirements to run project.
	@pip install -r requirements.txt --upgrade

build: ## Build the package
	@python -m build --sdist

black: ## Run black utility to format source files
	@black --check clappform

mypy: ## Run mypy utility to static type check
	@mypy clappform

pylint: ## Run pylint utility to check source files
	@pylint clappform

flake8: ## Run flake8 utility to check source files
	@flake8 clappform

ruff: ## Run ruff utility to check source files
	@ruff check --no-fix --no-unsafe-fixes clappform
	@ruff format --check clappform

lint: black mypy pylint flake8 ruff ## Lint a whole project

clean: ## Delete all temporary files
	@find clappform -type f -name '*.py[cod]' -delete
	@find clappform -type d -name '__pycache__' -delete
	@rm -rf *.egg *.egg-info build dist public
