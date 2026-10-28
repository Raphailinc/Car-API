# Car API

[![CI](https://github.com/Raphailinc/Car-API/actions/workflows/ci.yml/badge.svg)](https://github.com/Raphailinc/Car-API/actions/workflows/ci.yml)

[English](README.md) · [Русский](README.ru.md)

Компактный backend-проект каталога автомобилей: валидация схемы, ограничения БД и предсказуемые ответы CRUD API.

## Возможности

- Marshmallow проверяет входные данные и принимает ключи enum либо отображаемые значения.
- VIN генерируется при отсутствии; уникальность гарантируется БД.
- Локально используется SQLite, в Docker Compose — PostgreSQL.
- Pytest проверяет CRUD, некорректные значения, уникальность VIN и административное удаление.

## Локальный запуск

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
cp .env.example .env
python manage.py
```

## Проверки

```bash
python -m pytest
ruff check .
black --check .
```

## Условия запуска и границы проекта

API: http://localhost:8000/cars. Требуется Python 3.11+. В .env.example DATABASE_URL оставлен закомментированным: локальный запуск использует SQLite, Compose задаёт PostgreSQL. Массовое удаление выключено без ADMIN_TOKEN и требует заголовок X-Admin-Token. Обычный CRUD не имеет пользовательской аутентификации: это локальный пример API, а не публичный многопользовательский сервис. Схема отклоняет некорректные годы, неположительную мощность, пустые названия и пустой VIN при обновлении.

## Пример API

```bash
curl -X POST http://localhost:8000/cars \
  -H 'Content-Type: application/json' \
  -d '{"brand":"Toyota","model":"MODEL_A","year":2023,"color":"blue","engine_power":150,"configuration":"COMFORT"}'
```

`GET /cars` — список; `PUT /cars/<id>` — обновление; `DELETE /cars/<id>` — удаление. Допустимые значения описаны в [схеме](kanban/schemas.py).
