.PHONY: run up down logs shell dev-clean

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

dev-clean:
	docker-compose down -v --remove-orphans
	docker system prune -f
