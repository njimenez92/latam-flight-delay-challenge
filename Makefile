.ONESHELL:

.PHONY: help
help:             	## Muestra la ayuda
	@echo "Uso: make <objetivo>"
	@echo "Objetivos disponibles:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

.PHONY: install-pyenv
install-pyenv:    ## Instala pyenv (sistemas Unix)
	@echo "Instalando pyenv..."
	@if command -v pyenv >/dev/null 2>&1; then \
		echo "pyenv ya está instalado."; \
	else \
		curl https://pyenv.run | bash; \
		echo 'export PYENV_ROOT="$$HOME/.pyenv"' >> $$HOME/.bashrc; \
		echo 'export PATH="$$PYENV_ROOT/bin:$$PATH"' >> $$HOME/.bashrc; \
		echo 'eval "$$(pyenv init --path)"' >> $$HOME/.bashrc; \
		echo 'eval "$$(pyenv init -)"' >> $$HOME/.bashrc; \
		echo 'eval "$$(pyenv virtualenv-init -)"' >> $$HOME/.bashrc; \
		source $$HOME/.bashrc; \
		echo "pyenv instalado correctamente."; \
	fi

.PHONY: install-python
install-python:   ## Instala una versión específica de Python con pyenv
	@echo "Instalando Python 3.11.11..."
	@if pyenv versions | grep -q 3.11.11; then \
		echo "Python 3.11.11 ya está instalado."; \
	else \
		pyenv install 3.11.11; \
		echo "Python 3.11.11 instalado correctamente."; \
	fi

.PHONY: install-poetry
install-poetry:   ## Instala Poetry
	@echo "Instalando Poetry..."
	@if command -v poetry >/dev/null 2>&1; then \
		echo "Poetry ya está instalado."; \
	else \
		curl -sSL https://install.python-poetry.org | python3 -; \
		echo "Poetry instalado correctamente."; \
	fi

.PHONY: setup-env
setup-env: install-pyenv install-python install-poetry ## Configura el entorno de desarrollo

.PHONY: install
install:		## Instala las dependencias con Poetry
	poetry install

.PHONY: model-test
model-test:		## Ejecuta las pruebas del modelo
	mkdir -p reports
	poetry run pytest --cov-config=.coveragerc --cov-report term \
					  --cov-report html:reports/html \
					  --cov-report xml:reports/coverage.xml \
					  --junitxml=reports/junit.xml \
					  --cov=challenge tests/model

.PHONY: api-test
api-test:		## Ejecuta las pruebas de la API
	mkdir -p reports
	poetry run pytest --cov-config=.coveragerc --cov-report term \
					  --cov-report html:reports/html \
					  --cov-report xml:reports/coverage.xml \
					  --junitxml=reports/junit.xml \
					  --cov=challenge tests/api

.PHONY: utils-test
utils-test:		## Ejecuta las pruebas de la Utils de la API
	mkdir -p reports
	poetry run pytest --cov-config=.coveragerc --cov-report term \
					  --cov-report html:reports/html \
					  --cov-report xml:reports/coverage.xml \
					  --junitxml=reports/junit.xml \
					  --cov=utils tests/utils

STRESS_URL = http://127.0.0.1:8000
.PHONY: stress-test
stress-test:	## Ejecuta pruebas de estrés con Locust
	mkdir -p reports
	poetry run locust -f tests/stress/api_stress.py --print-stats \
					  --html reports/stress-test.html --run-time 60s \
					  --headless --users 100 --spawn-rate 1 \
					  -H $(STRESS_URL)

.PHONY: build
build:			## Construye el artefacto wheel con Poetry
	poetry build