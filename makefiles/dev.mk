.PHONY: dev-run dev-up dev-down dev-logs dev-shell dev-migrate dev-makemigrations dev-clean dev-test

UID=$(shell id -u)
DOCKER_COMPOSE_CMD = env UID=$(UID) docker compose

dev-build:
	$(DOCKER_COMPOSE_CMD) build

dev-run:
	$(DOCKER_COMPOSE_CMD) up

dev-up:
	$(DOCKER_COMPOSE_CMD) up -d --build

dev-down:
	$(DOCKER_COMPOSE_CMD) down

dev-logs:
	$(DOCKER_COMPOSE_CMD) logs -f

dev-shell:
	$(DOCKER_COMPOSE_CMD) run --rm --entrypoint /bin/sh web

dev-migrate:
	$(DOCKER_COMPOSE_CMD) run --rm --entrypoint /app/.venv/bin/python web manage.py migrate

dev-makemigrations:
	$(DOCKER_COMPOSE_CMD) run --rm --entrypoint /app/.venv/bin/python web manage.py makemigrations

dev-clean:
	$(DOCKER_COMPOSE_CMD) down -v --remove-orphans
	$(DOCKER_COMPOSE_CMD) system prune -f

dev-lint-fix:
	$(DOCKER_COMPOSE_CMD) run --rm --entrypoint /app/.venv/bin/ruff web check --no-cache lung_cancer_screening --fix
