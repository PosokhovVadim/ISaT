FROM python:3.11

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock /app/

RUN poetry install  --no-interaction --no-ansi

COPY . /app/