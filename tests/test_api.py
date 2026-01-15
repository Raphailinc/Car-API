import json
import pytest

from kanban import create_app, db
from kanban.models import Car


@pytest.fixture()
def client():
    app = create_app()
    app.config.update(
        SQLALCHEMY_DATABASE_URI="sqlite://",
        TESTING=True,
    )
    with app.app_context():
        db.create_all()
    yield app.test_client()


def test_create_and_get_car(client):
    payload = {
        "brand": "Toyota",
        "model": "Модель A",
        "year": 2022,
        "color": "blue",
        "engine_power": 200,
        "configuration": "Комфорт",
        "description": "Test car",
    }
    res = client.post("/cars", data=json.dumps(payload), content_type="application/json")
    assert res.status_code == 201
    car = res.get_json()
    assert car["brand"] == "Toyota"

    res = client.get("/cars")
    assert res.status_code == 200
    data = res.get_json()
    assert len(data["cars"]) == 1
    assert data["cars"][0]["brand"] == "Toyota"


def test_unique_vin(client):
    base = {
        "brand": "Ford",
        "model": "Модель B",
        "year": 2020,
        "color": "red",
        "engine_power": 150,
        "configuration": "Базовая",
        "vin": "ABC12345678901234",
    }
    res1 = client.post("/cars", data=json.dumps(base), content_type="application/json")
    assert res1.status_code == 201
    res2 = client.post("/cars", data=json.dumps(base), content_type="application/json")
    assert res2.status_code == 400
    assert "VIN" in res2.get_json()["message"]
