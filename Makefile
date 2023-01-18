up:
	make build
	make start
	make admin-up
	make start-load-data-to-elastic

build:
	docker-compose build --no-cache

start:
	docker-compose up -d

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
	docker-compose exec etl sh -c "python etl.py"

stop:
	docker-compose stop

remove:
	docker-compose down

remove-all:
	docker-compose down -v
