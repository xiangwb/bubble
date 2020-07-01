.PHONY: init build run test tox pyc cython

init:  build run
	docker-compose exec web bubble db upgrade
	docker-compose exec web bubble init
	@echo "Init done, containers running"

build:
	docker-compose build

run:
	docker-compose up -d

test:
	docker-compose stop celery # stop celery to avoid conflicts with celery tests
	docker-compose start redis # ensuring both redis are started
	docker-compose run -v $(PWD)/tests:/code/tests:ro web tox -e test
	docker-compose start celery

tox:
	docker-compose stop celery # stop celery to avoid conflicts with celery tests
	docker-compose start redis # ensuring both redis are started
	docker-compose run -v $(PWD)/tests:/code/tests:ro web tox -e py38
	docker-compose start celery

lint:
	docker-compose run web tox -e lint

pyc:
	python3 generate_deploy_pyc.py

cython:
	python3 generate_cython.py