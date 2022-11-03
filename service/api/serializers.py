from rest_marshmallow import Schema, fields


class BuildingSerializer(Schema):
    id = fields.String()
    name = fields.String()
    number = fields.Int()
    association_name = fields.String()
    city = fields.String()
    street = fields.String()
    street_number = fields.String(max_length=16)


class ApartmentSerializer(Schema):
    id = fields.String()
    rooms = fields.Int()
    floor = fields.Int()
    area = fields.Int()
    rent = fields.Int()
    building = fields.Nested(BuildingSerializer)
    latitude = fields.Str()
    longitude = fields.Str()
    description = fields.String()


class UserSerializer(Schema):
    full_name = fields.String()


class RentalAgreementSerializer(Schema):
    id = fields.String()
    owner = fields.Nested(UserSerializer)
    tenant = fields.Nested(UserSerializer)
    building = fields.Nested(BuildingSerializer)
    apartment = fields.Nested(ApartmentSerializer)
    signed_at = fields.String()
    start_at = fields.String()
    end_at = fields.String()
    is_renewable = fields.Bool()
