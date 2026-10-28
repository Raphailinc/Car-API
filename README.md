# Car API

[![CI](https://github.com/Raphailinc/Car-API/actions/workflows/ci.yml/badge.svg)](https://github.com/Raphailinc/Car-API/actions/workflows/ci.yml)

[English](README.md) · [Русский](README.ru.md)

A compact backend portfolio project for a car catalog. It demonstrates schema validation, database constraints and predictable CRUD responses.

## What it does

- Validate car payloads with Marshmallow and accept enum keys or display values.
- Generate a VIN when omitted and enforce uniqueness in the database.
- Use SQLite locally or PostgreSQL through Docker Compose.
- Exercise CRUD, invalid input and administrative deletion with isolated pytest fixtures.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
cp .env.example .env
python manage.py
```

## Checks

```bash
python -m pytest
ruff check .
black --check .
```

## Scope and implementation notes

Local API: `http://localhost:8000/cars`. This is a portfolio CRUD service. Bulk deletion requires `X-Admin-Token` and is disabled when `ADMIN_TOKEN` is empty. Configure credentials and origins before exposing a deployment.

## API example

```bash
curl -X POST http://localhost:8000/cars \
  -H 'Content-Type: application/json' \
  -d '{"brand":"Toyota","model":"MODEL_A","year":2023,"color":"blue","engine_power":150,"configuration":"COMFORT"}'
```

`GET /cars` lists cars, `PUT /cars/<id>` updates a record and `DELETE /cars/<id>` removes one. See [`kanban/schemas.py`](kanban/schemas.py) for accepted values and validation.
