import uuid


class BuildingValidator:
    def __init__(self, **kwargs):
        self.id: str = kwargs.get("id")
        self.name: str = kwargs.get("name")
        self.number: int = kwargs.get("number")
        self.association_name: str = kwargs.get("association_name")
        self.city: str = kwargs.get("city")
        self.street: str = kwargs.get("street")
        self.street_number: str = kwargs.get("street_number")
        self.user_id: int = kwargs.get("user_id")

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = str(uuid.uuid4())

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise ValueError("Name should be string")
        if len(value) > 100:
            raise ValueError("Name cannot exceed 100 characters.")
        self._name = value

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, value):
        if not isinstance(value, int):
            raise ValueError("Number should be int")
        if value < 1:
            raise ValueError("Number should positive integer")
        self._number = value

    @property
    def association_name(self):
        return self._association_name

    @association_name.setter
    def association_name(self, value):
        if not isinstance(value, str):
            raise ValueError("Association name should be string")
        if len(value) > 100:
            raise ValueError("Association name cannot exceed 100 characters.")
        self._association_name = value

    @property
    def city(self):
        return self._city

    @city.setter
    def city(self, value):
        if not isinstance(value, str):
            raise ValueError("City should be string")
        if len(value) > 128:
            raise ValueError("City cannot exceed 128 characters.")
        self._city = value

    @property
    def street(self):
        return self._street

    @street.setter
    def street(self, value):
        if not isinstance(value, str):
            raise ValueError("Stree should be string.")
        if len(value) > 128:
            raise ValueError("Stree cannot exceed 128 characters.")
        self._street = value

    @property
    def street_number(self):
        return self._street_number

    @street_number.setter
    def street_number(self, value):
        if not isinstance(value, str):
            raise ValueError("Street number should be string.")
        if len(value) > 16:
            raise ValueError("Street number cannot exceed 16 characters.")
        self._street_number = value

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, value):
        if not isinstance(value, int):
            raise ValueError("Invalid user_id")
        self._user_id = value

    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "number": self.number,
            "association_name": self.association_name,
            "city": self.city,
            "street": self.street,
            "street_number": self.street_number,
            "user_id": self.user_id,
        }
