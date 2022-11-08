import uuid

from marshmallow import Schema, fields


class ApartmentBase(Schema):
    user_id = fields.String()
    building_id = fields.String()
    rooms = fields.Int()
    floor = fields.Int()
    area = fields.Int()
    rent = fields.Int()
    building = fields.Str()
    latitude = fields.Decimal()
    longitude = fields.Decimal()
    description = fields.String()


class CreateApartment(ApartmentBase):
    id = fields.Method("generate_uuid")

    def generate_uuid(self, data):
        return str(uuid.uuid4())[:10]


class UpdateApartment(ApartmentBase):
    pass


class BuildingBase(Schema):
    user_id = fields.String()
    name = fields.String()
    number = fields.Int()
    association_name = fields.String()
    city = fields.String()
    street = fields.String()
    street_number = fields.String(max_length=16)


class CreateBuilding(BuildingBase):
    id = fields.Method("generate_uuid")

    def generate_uuid(self, data):
        return str(uuid.uuid4())


class UpdateBuilding(BuildingBase):
    pass


class RentalAgreementBase(Schema):
    user_id = fields.String()
    owner_id = fields.String()
    tenant_id = fields.String()
    building_id = fields.String()
    apartment_id = fields.String()
    signed_at = fields.String()
    start_at = fields.String()
    end_at = fields.String()
    is_renewable = fields.Bool()


class CreateRentalAgreement(RentalAgreementBase):
    id = fields.Method("generate_uuid")

    def generate_uuid(self, data):
        return str(uuid.uuid4())


class UpdateRentalAgreement(RentalAgreementBase):
    pass
