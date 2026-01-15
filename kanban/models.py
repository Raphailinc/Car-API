from enum import Enum

from . import db


class CarModelEnum(Enum):
    MODEL_A = "Модель A"
    MODEL_B = "Модель B"
    MODEL_C = "Модель C"


class CarConfiguration(Enum):
    BASE = "Базовая"
    COMFORT = "Комфорт"
    MAXIMUM = "Максимальная"


class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(50), nullable=False)
    model = db.Column(db.Enum(CarModelEnum), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    color = db.Column(db.String(20), nullable=False)
    engine_power = db.Column(db.Integer, nullable=False)
    vin = db.Column(db.String(17), unique=True, nullable=False)
    configuration = db.Column(db.Enum(CarConfiguration), nullable=False)
    description = db.Column(db.Text)

    def to_dict(self):
        return {
            "id": self.id,
            "brand": self.brand,
            "model": self.model.value,
            "year": self.year,
            "color": self.color,
            "engine_power": self.engine_power,
            "vin": self.vin,
            "configuration": self.configuration.value,
            "description": self.description,
        }
