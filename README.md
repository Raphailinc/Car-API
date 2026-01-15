![CI](https://github.com/Raphailinc/Car-API/actions/workflows/ci.yml/badge.svg)
![Coverage](https://img.shields.io/codecov/c/github/Raphailinc/Car-API?label=coverage)

# Car API

Flask API для CRUD по автомобилям с валидацией (Marshmallow) и конфигом через `.env`. По умолчанию использует SQLite, для продакшена рекомендован PostgreSQL.

## Quickstart (Docker)
```bash
cp .env.example .env          # при необходимости правим DATABASE_URL/PORT
docker compose up --build
# API будет на http://localhost:8000/cars
```

## Локальная разработка
```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env          # можно оставить SQLite или указать свой PostgreSQL
python manage.py              # запустит на 0.0.0.0:8000
```

Линт и тесты:
```bash
ruff check .
black --check .
pytest
```

## API
- `GET /cars` — список машин.
- `POST /cars` — создать (JSON: brand, model, year, color, engine_power, configuration, vin?, description).
- `PUT /cars/<id>` — обновить (частичный payload).
- `DELETE /cars/<id>` — удалить.
- `DELETE /cars/delete-all` — удалить все.

### Пример запроса/ответа
```bash
POST /cars
{
  "brand": "Toyota",
  "model": "Модель A",
  "year": 2022,
  "color": "blue",
  "engine_power": 200,
  "configuration": "Комфорт"
}
```
Ответ `201`:
```json
{"id":1,"brand":"Toyota","model":"Модель A","year":2022,"color":"blue","engine_power":200,"vin":"<auto>","configuration":"Комфорт","description":null}
```

## Архитектура
- `kanban/` — app factory, модели, схемы Marshmallow, маршруты `/cars`, утилиты (VIN).
- `manage.py` — точка входа (локально/в Docker), создаёт БД при старте.
- `tests/` — pytest с SQLite in-memory, покрывает CRUD и уникальность VIN.
- `.env`/`config.py` — загрузка DATABASE_URL, переключение SQLite/Postgres.

## Quality
- Линт: `ruff check .`
- Формат: `black --check .`
- Тесты: `pytest` (in-memory SQLite)
- CI: GitHub Actions (`ci.yml`) — lint + tests на Python 3.11.

## Интеграция
Пример вызова API из Python:
```python
import requests

base = "http://localhost:8000"
car = {
    "brand": "Toyota",
    "model": "Модель A",
    "year": 2023,
    "color": "blue",
    "engine_power": 200,
    "configuration": "Комфорт",
}
resp = requests.post(f"{base}/cars", json=car, timeout=5)
resp.raise_for_status()
print(resp.json())
```

Значения `model`: `Модель A|Модель B|Модель C`. `configuration`: `Базовая|Комфорт|Максимальная`. VIN проверяется на длину 17, при отсутствии генерируется автоматически.

## Тесты
```bash
pytest
```

## Примечания
- Конфиг загружается из `.env` (см. `.env.example`).
- В Docker Compose используется PostgreSQL (`DATABASE_URL` по умолчанию указывает на сервис `db`); локально можно оставить SQLite.
- База создаётся автоматически при старте.
- Уникальность VIN соблюдается.
