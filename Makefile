test-local:
	docker-compose down
	docker-compose -f docker-compose.local-testing.yml up -d
	python fastapi/src/main.py

make run-tests:
	docker-compose down
	docker-compose -f docker-compose.testing.yml up --attach tests --exit-code-from tests


up:
	make build
	make start
	make admin-up
	make start-load-data-to-elastic

dev-up:
	make dev-build
	make dev-start
	make admin-up

build:
	docker-compose build --no-cache

dev-build:
	docker-compose -f docker-compose.dev.yml build --no-cache

start:
	docker-compose up -d

dev-start:
	docker-compose -f docker-compose.dev.yml up -d

fake-migrate:
	docker-compose exec movies_admin python manage.py migrate --no-input --fake movies

system-migrate:
	docker-compose exec movies_admin python manage.py migrate --no-input

migrate:
	make fake-migrate
	make system-migrate

superuser:
	docker-compose exec movies_admin python manage.py createsuperuser --username admin --email admin@email.com --no-input

static:
	docker-compose exec movies_admin python manage.py collectstatic --no-input --clear

admin-up:
	make migrate
	make static
	make superuser

start-load-data-to-elastic:
	docker-compose exec -d etl sh -c "python etl.py"

stop:
	docker-compose stop

remove:
	docker-compose down

remove-all:
	docker-compose down -v

force-remove:
	docker-compose down --remove-orphans -v
