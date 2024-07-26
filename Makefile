all: clean lint build test

build:
	docker compose build router
	docker compose run --rm router pip freeze > requirements.txt

changelog:
	PYTHONPATH=. gitchangelog > CHANGELOG.md

clean:
	docker compose down -t 0

cleanall: clean
	docker system prune --all --force --volumes

lint:
	docker run --rm -i hadolint/hadolint < Dockerfile
	isort -v .
	flake8

tag:
	@python -c 'import router; print(router.__version__)'

test:
	LOG_LEVEL=DEBUG PYTHONPATH=.:.. pytest
	docker compose up -d --wait

update-requirements:
	pip freeze > /tmp/requirements.txt
	comm -23 /tmp/requirements.txt ./requirements.txt > requirements-dev.txt
