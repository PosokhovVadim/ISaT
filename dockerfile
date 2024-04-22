FROM python:3.11

WORKDIR /app

RUN apt-get update && apt-get install -y sqlite3

RUN pip install poetry

COPY pyproject.toml poetry.lock /app/

RUN poetry install  --no-interaction --no-ansi

COPY . /app/