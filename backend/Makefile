export PYTHONPATH := .
PYTEST_WORKERS_CONCURRENCY ?= 8

.PHONY: help
help:
	@echo 'Available Commands:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf " - \033[36m%-18s\033[0m %s\n", $$1, $$2}'

.PHONY: all
all: fix-imports lint lint-ci gitlint test  ## Run all the lint and test phases in order

.PHONY: setup
setup: ## Create python virtual environment and install prerequisites
	@poetry export --only=main --output requirements.txt --without-hashes && pip install --no-cache-dir -r requirements.txt

.PHONY: lint
lint: ## Run flake8 and mypy linters
	@echo "=== Checking code style ==="
	@poetry run flake8 .
	@echo "=== Checking code hints ==="
	@poetry run mypy --install-types --non-interactive --namespace-packages src

.PHONY: lint-ci
lint-ci: ## Run flake8 and mypy linters like CI would do
	@echo "=== Checking code style ==="
	@poetry run flake8 --format=gl-codeclimate . > code-quality-report.json
	@echo "=== Checking code hints ==="
	@poetry run mypy --install-types --non-interactive --namespace-packages src

.PHONY: fix-imports
fix-imports:
	@poetry run isort --skip .venv --skip venv .

.PHONY: run-dev
run-dev: ## Run django development server
	    @poetry run src/manage.py runserver

.PHONY: run-celery-worker-default
run-celery-worker-default: ## Run celery worker for general purpose tasks
		@cd src && poetry run python -m celery -A job_journey worker -l INFO -n "local-default" -E

.PHONY: run-celery-beat
run-celery-beat: ## Run celery beat scheduler
		@cd src && poetry run python -m celery -A job_journey beat -l INFO

.PHONY: test
test: ## Run tests
	  @PYTEST_WORKERS_CONCURRENCY=${PYTEST_WORKERS_CONCURRENCY:-8} \
	  poetry run pytest -n ${PYTEST_WORKERS_CONCURRENCY} --create-db --cache-clear --showlocals --verbose --cov=src --cov-config=.coveragerc --cov-report="term-missing"

.PHONY: migrate
migrate:    ## Run django migrations
	    @poetry run src/manage.py migrate

.PHONY: shell
shell: ## Access the Django shell in your terminal
	  @poetry run src/manage.py shell

.PHONY: makemigrations
makemigrations: ## Generates Django migrations
	  @poetry run src/manage.py makemigrations

.PHONY: create-admin
create-admin:    ## Create Django Super Admin
	    @DJANGO_SUPERUSER_PASSWORD=123 poetry run src/manage.py createsuperuser --noinput --email admin@jobjourney.com

.PHONY: delete-migrations
delete-migrations: ## Delete all migration files
	  find . -path "./src/*/migrations/*.py" -not -name "__init__.py" -delete
