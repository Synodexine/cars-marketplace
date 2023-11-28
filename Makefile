up:
	docker-compose up

build:
	docker-compose build

down:
	docker-compose down

test:
	docker-compose exec app python manage.py test

run:
	docker-compose exec app python manage.py $(command)
