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
	$(DOCKER_COMPOSE_CMD) run --rm web bash

dev-migrate:
	$(DOCKER_COMPOSE_CMD) run --rm web python manage.py migrate

dev-makemigrations:
	$(DOCKER_COMPOSE_CMD) run --rm web python manage.py makemigrations

dev-clean:
	$(DOCKER_COMPOSE_CMD) down -v --remove-orphans
	$(DOCKER_COMPOSE_CMD) system prune -f

dev-test:
	$(DOCKER_COMPOSE_CMD) run --rm web python manage.py test

dev-lint-fix:
	$(DOCKER_COMPOSE_CMD) run --rm web poetry run ruff check --no-cache lung_cancer_screening --fix
