# syntax=docker/dockerfile:1.2
FROM python:3.11-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos de Poetry
COPY pyproject.toml poetry.lock ./

# Instalar Poetry
RUN pip install --upgrade pip
RUN pip install poetry

# Instalar las dependencias sin las de desarrollo
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

# Copiar el resto del código
COPY challenge/ ./challenge/
COPY tests/ ./tests/
COPY data/ ./data/
COPY Makefile ./


# Exponer el puerto que usará la aplicación
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "challenge.api:app", "--host", "0.0.0.0", "--port", "8000"]
