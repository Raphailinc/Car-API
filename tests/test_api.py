import pytest

from kanban import create_app, db


def base_payload(**overrides):
    payload = {
        "brand": "Toyota",
        "model": "MODEL_A",
        "year": 2022,
        "color": "blue",
        "engine_power": 200,
        "configuration": "COMFORT",
        "description": "Test car",
    }
    payload.update(overrides)
    return payload


@pytest.fixture()
def make_client():
    def _create_client(
        admin_token="admin-secret",
        cors_origins=None,
        trusted_origins=None,
    ):
        app = create_app(
            {
                "SQLALCHEMY_DATABASE_URI": "sqlite://",
                "TESTING": True,
                "ADMIN_TOKEN": admin_token,
                "CORS_ORIGINS": cors_origins or ["http://localhost"],
                "CORS_TRUSTED_ORIGINS": trusted_origins or ["http://localhost"],
            }
        )
        with app.app_context():
            db.create_all()
        return app.test_client()

    return _create_client


@pytest.fixture()
def client(make_client):
    return make_client()


def test_enum_serialization_create_list_update(client):
    res = client.post("/cars", json=base_payload())
    assert res.status_code == 201
    car = res.get_json()
    assert car["model"] == "Модель A"
    assert car["configuration"] == "Комфорт"

    list_res = client.get("/cars")
    assert list_res.status_code == 200
    data = list_res.get_json()
    assert data["cars"][0]["model"] == "Модель A"
    assert data["cars"][0]["configuration"] == "Комфорт"

    update_res = client.put(
        f"/cars/{car['id']}", json={"model": "MODEL_B", "configuration": "MAXIMUM"}
    )
    assert update_res.status_code == 200
    updated = update_res.get_json()
    assert updated["model"] == "Модель B"
    assert updated["configuration"] == "Максимальная"


def test_enum_deserialization_accepts_human_values(client):
    payload = base_payload(model="Модель C", configuration="Максимальная")
    res = client.post("/cars", json=payload)
    assert res.status_code == 201
    car = res.get_json()
    assert car["model"] == "Модель C"
    assert car["configuration"] == "Максимальная"


def test_validation_brand_length(client):
    res = client.post("/cars", json=base_payload(brand="a" * 51))
    assert res.status_code == 400
    data = res.get_json()
    assert data["error"] == "ValidationError"
    assert data["fields"]["brand"] == ["Max length is 50"]


def test_validation_color_length(client):
    res = client.post("/cars", json=base_payload(color="c" * 21))
    assert res.status_code == 400
    data = res.get_json()
    assert data["error"] == "ValidationError"
    assert data["fields"]["color"] == ["Max length is 20"]


def test_vin_validation_and_uniqueness(client):
    short_vin_res = client.post("/cars", json=base_payload(vin="123"))
    assert short_vin_res.status_code == 400
    data = short_vin_res.get_json()
    assert data["fields"]["vin"] == ["vin must be 17 characters"]

    payload = base_payload(vin="A" * 17)
    res1 = client.post("/cars", json=payload)
    assert res1.status_code == 201
    res2 = client.post("/cars", json=payload)
    assert res2.status_code == 400
    assert res2.get_json()["fields"]["vin"] == ["VIN must be unique"]


def test_auto_vin_generation_unique_and_length(client):
    vins = set()
    for idx in range(5):
        res = client.post("/cars", json=base_payload(brand=f"Brand{idx}"))
        assert res.status_code == 201
        vin = res.get_json()["vin"]
        assert len(vin) == 17
        assert vin not in vins
        vins.add(vin)


def test_update_and_delete_single_car_flow(client):
    create_res = client.post("/cars", json=base_payload())
    car_id = create_res.get_json()["id"]

    update_res = client.put(
        f"/cars/{car_id}",
        json={"brand": "Subaru", "color": "green", "model": "Модель C"},
    )
    assert update_res.status_code == 200
    updated = update_res.get_json()
    assert updated["brand"] == "Subaru"
    assert updated["color"] == "green"
    assert updated["model"] == "Модель C"

    delete_res = client.delete(f"/cars/{car_id}")
    assert delete_res.status_code == 200
    list_res = client.get("/cars")
    assert list_res.get_json()["cars"] == []


def test_delete_all_security_without_token(make_client):
    client = make_client(admin_token=None)
    res = client.delete("/cars/delete-all")
    assert res.status_code == 404


def test_delete_all_security_wrong_token(make_client):
    client = make_client(admin_token="secret-token")
    res = client.delete("/cars/delete-all", headers={"X-Admin-Token": "invalid"})
    assert res.status_code == 403
    data = res.get_json()
    assert data["message"] == "Admin token required"


def test_delete_all_security_success(make_client):
    client = make_client(admin_token="secret-token")
    res = client.post("/cars", json=base_payload())
    assert res.status_code == 201

    res = client.delete("/cars/delete-all", headers={"X-Admin-Token": "secret-token"})
    assert res.status_code == 200
    list_res = client.get("/cars")
    assert list_res.get_json()["cars"] == []


def test_delete_origin_restricted(make_client):
    client = make_client(
        admin_token="secret-token",
        cors_origins=["http://localhost"],
        trusted_origins=["http://localhost"],
    )
    res = client.post("/cars", json=base_payload())
    car_id = res.get_json()["id"]

    delete_res = client.delete(f"/cars/{car_id}", headers={"Origin": "http://evil.com"})
    assert delete_res.status_code == 403
