from marshmallow import Schema, ValidationError, fields, validates, validates_schema
from marshmallow_enum import EnumField

from .models import CarConfiguration, CarModelEnum


class FlexibleEnumField(EnumField):
    """Enum field that dumps human value and accepts enum key or value."""

    def __init__(self, enum, **kwargs):
        super().__init__(enum, by_value=True, **kwargs)
        self.enum_cls = enum

    def _error_message(self) -> str:
        keys = ", ".join(self.enum_cls.__members__.keys())
        values = ", ".join(member.value for member in self.enum_cls)
        return f"Must be one of: {keys} or {values}"

    def _deserialize(self, value, attr, data, **kwargs):
        # Allow enum instances, keys (MODEL_A) and human values.
        if isinstance(value, self.enum_cls):
            return value
        if isinstance(value, str):
            if value in self.enum_cls.__members__:
                return self.enum_cls[value]
            for member in self.enum_cls:
                if value == member.value:
                    return member
        raise ValidationError(self._error_message())

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        if isinstance(value, self.enum_cls):
            return value.value
        if isinstance(value, str):
            if value in self.enum_cls.__members__:
                return self.enum_cls[value].value
            for member in self.enum_cls:
                if value == member.value:
                    return value
        raise ValidationError(self._error_message())


class CarSchema(Schema):
    id = fields.Integer(dump_only=True)
    brand = fields.Str(required=True)
    model = FlexibleEnumField(CarModelEnum, required=True)
    year = fields.Int(required=True)
    color = fields.Str(required=True)
    engine_power = fields.Int(required=True)
    vin = fields.Str(required=False, allow_none=False)
    configuration = FlexibleEnumField(CarConfiguration, required=True)
    description = fields.Str(allow_none=True)

    @validates("brand")
    def validate_brand(self, value):
        self._validate_length("brand", value, 1, 50)

    @validates("color")
    def validate_color(self, value):
        self._validate_length("color", value, 1, 20)

    @validates("vin")
    def validate_vin(self, value):
        if value and len(value) != 17:
            raise ValidationError("vin must be 17 characters")

    @validates_schema
    def validate_year(self, data, **kwargs):
        year = data.get("year")
        if year and (year < 1900 or year > 2100):
            raise ValidationError("year must be between 1900 and 2100", field_name="year")

    @staticmethod
    def _validate_length(field_name: str, value: str, min_len: int, max_len: int) -> None:
        if value is None:
            raise ValidationError("Field may not be null.")
        if len(value) < min_len:
            raise ValidationError(f"Min length is {min_len}")
        if len(value) > max_len:
            raise ValidationError(f"Max length is {max_len}")
