from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError

from . import db
from .models import Car, CarConfiguration, CarModelEnum
from .schemas import CarSchema
from .utils import generate_vin

bp = Blueprint("api", __name__, url_prefix="/cars")
car_schema = CarSchema()
cars_schema = CarSchema(many=True)


@bp.route("", methods=["GET"])
def list_cars():
    cars = Car.query.order_by(Car.id.desc()).all()
    return jsonify({"cars": cars_schema.dump(cars)})


@bp.route("", methods=["POST"])
def create_car():
    payload = request.get_json() or {}
    errors = car_schema.validate(payload)
    if errors:
        return jsonify({"errors": errors}), 400

    model_enum = CarModelEnum(payload["model"])
    config_enum = CarConfiguration(payload["configuration"])

    vin = payload.get("vin") or generate_vin()

    car = Car(
        brand=payload["brand"],
        model=model_enum,
        year=payload["year"],
        color=payload["color"],
        engine_power=payload["engine_power"],
        vin=vin,
        configuration=config_enum,
        description=payload.get("description"),
    )
    try:
        db.session.add(car)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "VIN должен быть уникальным"}), 400

    return jsonify(car_schema.dump(car)), 201


@bp.route("/<int:car_id>", methods=["PUT"])
def update_car(car_id):
    car = Car.query.get_or_404(car_id)
    payload = request.get_json() or {}
    errors = car_schema.validate(payload, partial=True)
    if errors:
        return jsonify({"errors": errors}), 400

    if "model" in payload:
        car.model = CarModelEnum(payload["model"])
    if "configuration" in payload:
        car.configuration = CarConfiguration(payload["configuration"])

    for field in ["brand", "year", "color", "engine_power", "vin", "description"]:
        if field in payload:
            setattr(car, field, payload[field])

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "VIN должен быть уникальным"}), 400

    return jsonify(car_schema.dump(car))


@bp.route("/<int:car_id>", methods=["DELETE"])
def delete_car(car_id):
    car = Car.query.get_or_404(car_id)
    db.session.delete(car)
    db.session.commit()
    return jsonify({"message": "Car deleted"})


@bp.route("/delete-all", methods=["DELETE"])
def delete_all():
    db.session.query(Car).delete()
    db.session.commit()
    return jsonify({"message": "All cars deleted"})
