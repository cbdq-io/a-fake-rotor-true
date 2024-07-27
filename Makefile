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
	docker compose up -d --wait
	LOG_LEVEL=DEBUG PYTHONPATH=.:.. pytest

trivy:
	trivy image --severity HIGH,CRITICAL --ignore-unfixed router:latest

update-pip-requirements:
	pip freeze > /tmp/requirements.txt
	comm -23 /tmp/requirements.txt ./requirements.txt > requirements-dev.txt

update-trivy-ignore:
	trivy image --format json --ignore-unfixed --severity HIGH,CRITICAL router:latest | jq -r '.Results[1].Vulnerabilities[].VulnerabilityID' | sort -u | tee .trivyignore
