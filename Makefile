PYTHON ?= python
DOCKER_COMPOSE_BACKEND_DEV = backend/docker-compose.backend.dev.yml
DOCKER_COMPOSE_ALL = docker-compose.yml

.PHONY: pre-commit ruff ruff-fix \
        up-backend-dev down-backend-dev logs-backend-dev build-backend-dev \
        migrate makemigrations superuser \
        up-all down-all

# QA / Lint

pre-commit:
	uv run pre-commit run --all-files

ruff:
	uv run ruff check .

ruff-fix:
	uv run ruff check . --fix
	uv run ruff format .

# Django

migrate:
	docker compose exec web uv run python manage.py migrate

makemigrations:
	docker compose exec web uv run python manage.py makemigrations

superuser:
	docker compose exec web uv run python manage.py createsuperuser

# Docker: backend-dev

build-backend-dev:
	docker compose -f $(DOCKER_COMPOSE_BACKEND_DEV) build

up-backend-dev:
	docker compose -f $(DOCKER_COMPOSE_BACKEND_DEV) up -d

down-backend-dev:
	docker compose -f $(DOCKER_COMPOSE_BACKEND_DEV) down

logs-backend-dev:
	docker compose -f $(DOCKER_COMPOSE_BACKEND_DEV) logs -f

# Docker: all

up-all:
	docker compose -f $(DOCKER_COMPOSE_ALL) up -d

down-all:
	docker compose -f $(DOCKER_COMPOSE_ALL) down
