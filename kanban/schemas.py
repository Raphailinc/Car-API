from marshmallow import Schema, fields, ValidationError, validates, validates_schema
from .models import CarConfiguration, CarModelEnum


def enum_values(enum_cls):
    return [e.value for e in enum_cls]


class CarSchema(Schema):
    id = fields.Integer(dump_only=True)
    brand = fields.Str(required=True)
    model = fields.Str(required=True)
    year = fields.Int(required=True)
    color = fields.Str(required=True)
    engine_power = fields.Int(required=True)
    vin = fields.Str(required=False, allow_none=True)
    configuration = fields.Str(required=True)
    description = fields.Str(allow_none=True)

    @validates("model")
    def validate_model(self, value):
        if value not in enum_values(CarModelEnum):
            raise ValidationError(f"model must be one of {enum_values(CarModelEnum)}")

    @validates("configuration")
    def validate_configuration(self, value):
        if value not in enum_values(CarConfiguration):
            raise ValidationError(f"configuration must be one of {enum_values(CarConfiguration)}")

    @validates("vin")
    def validate_vin(self, value):
        if value and len(value) != 17:
            raise ValidationError("vin must be 17 characters")

    @validates_schema
    def validate_year(self, data, **kwargs):
        year = data.get("year")
        if year and (year < 1900 or year > 2100):
            raise ValidationError("year must be between 1900 and 2100", field_name="year")
