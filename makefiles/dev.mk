.PHONY: dev-run dev-up dev-down dev-logs dev-shell dev-migrate dev-makemigrations dev-clean

dev-run:
	docker-compose up --build

dev-up:
	docker-compose up -d --build

dev-down:
	docker-compose down

dev-logs:
	docker-compose logs -f

dev-shell:
	docker-compose run web sh

dev-migrate:
	docker-compose run web python manage.py migrate

dev-makemigrations:
	docker-compose run web python manage.py makemigrations

dev-clean:
	docker-compose down -v --remove-orphans
	docker system prune -f
