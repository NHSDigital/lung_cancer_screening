.PHONY: dev-run dev-up dev-down dev-logs dev-shell dev-migrate dev-makemigrations dev-clean dev-test

DOCKER_COMPOSE_CMD = docker compose

dev-build:
	$(DOCKER_COMPOSE_CMD) build

dev-run:
	$(DOCKER_COMPOSE_CMD) up --build

dev-up:
	$(DOCKER_COMPOSE_CMD) up -d --build

dev-down:
	$(DOCKER_COMPOSE_CMD) down

dev-logs:
	$(DOCKER_COMPOSE_CMD) logs -f

dev-shell:
	$(DOCKER_COMPOSE_CMD) run web sh

dev-migrate:
	$(DOCKER_COMPOSE_CMD) run --rm web python manage.py migrate

dev-makemigrations:
	$(DOCKER_COMPOSE_CMD) run --rm web python manage.py makemigrations

dev-clean:
	$(DOCKER_COMPOSE_CMD) down -v --remove-orphans
	$(DOCKER_COMPOSE_CMD) system prune -f

dev-test:
	$(DOCKER_COMPOSE_CMD) run --rm web python manage.py test
