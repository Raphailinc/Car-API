# Kanban — Car API

Flask API для CRUD по автомобилям с валидацией (Marshmallow) и конфигом через `.env`. По умолчанию использует SQLite, можно переключить на PostgreSQL через переменную `DATABASE_URL`.

## Установка и запуск
```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # при необходимости правим DATABASE_URL/PORT
python manage.py       # запустит на 8000
```

## API
- `GET /cars` — список машин.
- `POST /cars` — создать (JSON: brand, model, year, color, engine_power, configuration, vin?, description).
- `PUT /cars/<id>` — обновить (частичный payload).
- `DELETE /cars/<id>` — удалить.
- `DELETE /cars/delete-all` — удалить все.

Значения `model`: `Модель A|Модель B|Модель C`. `configuration`: `Базовая|Комфорт|Максимальная`. VIN проверяется на длину 17, при отсутствии генерируется автоматически.

## Тесты
```bash
pytest
```

## Примечания
- Конфиг загружается из `.env` (см. `.env.example`).
- База создаётся автоматически при старте.
- Уникальность VIN соблюдается.
