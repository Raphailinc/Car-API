from flask import Blueprint, current_app, jsonify, request
from marshmallow import ValidationError
from sqlalchemy.exc import DataError, IntegrityError

from . import db
from .models import Car
from .schemas import CarSchema
from .utils import generate_vin

bp = Blueprint("api", __name__, url_prefix="/cars")
car_schema = CarSchema()
cars_schema = CarSchema(many=True)


def validation_error_response(errors: dict[str, list[str]]):
    return jsonify({"error": "ValidationError", "fields": errors}), 400


def enforce_trusted_delete_origin():
    """Restrict destructive requests to trusted origins when Origin is present."""
    origin = request.headers.get("Origin")
    if not origin:
        return None
    trusted_origins = current_app.config.get("CORS_TRUSTED_ORIGINS", [])
    if origin not in trusted_origins:
        return jsonify({"error": "Forbidden", "message": "Origin not allowed"}), 403
    return None


@bp.route("", methods=["GET"])
def list_cars():
    cars = Car.query.order_by(Car.id.desc()).all()
    return jsonify({"cars": cars_schema.dump(cars)})


@bp.route("", methods=["POST"])
def create_car():
    payload = request.get_json() or {}
    try:
        data = car_schema.load(payload)
    except ValidationError as err:
        return validation_error_response(err.messages)

    vin = data.pop("vin", None) or generate_vin()

    car = Car(
        brand=data["brand"],
        model=data["model"],
        year=data["year"],
        color=data["color"],
        engine_power=data["engine_power"],
        vin=vin,
        configuration=data["configuration"],
        description=data.get("description"),
    )
    try:
        db.session.add(car)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return validation_error_response({"vin": ["VIN must be unique"]})
    except DataError:
        db.session.rollback()
        return validation_error_response({"_schema": ["Invalid data"]})

    return jsonify(car_schema.dump(car)), 201


@bp.route("/<int:car_id>", methods=["PUT"])
def update_car(car_id):
    car = Car.query.get_or_404(car_id)
    payload = request.get_json() or {}
    try:
        data = car_schema.load(payload, partial=True)
    except ValidationError as err:
        return validation_error_response(err.messages)

    for field, value in data.items():
        setattr(car, field, value)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return validation_error_response({"vin": ["VIN must be unique"]})
    except DataError:
        db.session.rollback()
        return validation_error_response({"_schema": ["Invalid data"]})

    return jsonify(car_schema.dump(car))


@bp.route("/<int:car_id>", methods=["DELETE"])
def delete_car(car_id):
    origin_error = enforce_trusted_delete_origin()
    if origin_error:
        return origin_error
    car = Car.query.get_or_404(car_id)
    db.session.delete(car)
    db.session.commit()
    return jsonify({"message": "Car deleted"})


@bp.route("/delete-all", methods=["DELETE"])
def delete_all():
    origin_error = enforce_trusted_delete_origin()
    if origin_error:
        return origin_error

    admin_token = current_app.config.get("ADMIN_TOKEN")
    if not admin_token:
        return jsonify({"error": "NotFound"}), 404

    provided_token = request.headers.get("X-Admin-Token")
    if not provided_token or provided_token != admin_token:
        return jsonify({"error": "Forbidden", "message": "Admin token required"}), 403

    db.session.query(Car).delete()
    db.session.commit()
    return jsonify({"message": "All cars deleted"})
