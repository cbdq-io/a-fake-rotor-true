all: clean lint build test

build:
	docker compose build router
	docker compose run --no-deps --rm router pip freeze > requirements.txt

changelog:
	PYTHONPATH=. gitchangelog > CHANGELOG.md

clean:
	docker compose down -t 0
	find . -name __pycache__ -type d -exec rm -rf {} \; -depth

cleanall: clean
	docker system prune --all --force --volumes

lint:
	docker run --rm -i hadolint/hadolint < Dockerfile
	isort -v .
	flake8

non-system-tests:
	LOG_LEVEL=DEBUG PYTHONPATH=.:.. pytest -m 'not system'

tag:
	@grep ^__version__ router.py | cut -d\' -f 2

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
