from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extrs_fields):
        if not email:
            raise ValueError(_("The email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extrs_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser):
    full_name = models.CharField(max_length=100)
    identity_number = models.IntegerField()
    email = models.EmailField(
        verbose_name=_("Email address"), max_length=255, unique=True
    )
    contact_number = models.CharField(max_length=15)
    city = models.CharField(max_length=128)
    street = models.CharField(max_length=128)
    street_number = models.CharField(max_length=16)
    zip = models.CharField(max_length=15)
    is_company = models.BooleanField(default=False)
    license_until = models.DateTimeField()
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = UserManager()
    USERNAME_FIELD = "email"


class Building(models.Model):
    id = models.CharField(primary_key=True, max_length=40)
    name = models.CharField(max_length=100)
    number = models.IntegerField()
    association_name = models.CharField(max_length=100)
    city = models.CharField(max_length=128)
    street = models.CharField(max_length=128)
    street_number = models.CharField(max_length=16)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Apartment(models.Model):
    id = models.CharField(primary_key=True, max_length=10)
    rooms = models.IntegerField()
    floor = models.IntegerField()
    area = models.IntegerField()
    rent = models.IntegerField()
    building = models.ForeignKey(Building, on_delete=models.CASCADE, null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def serialize(self):
        return {
            "id": self.id,
            "rooms": self.rooms,
            "floor": self.floor,
            "area": self.area,
            "rent": self.rent,
            "latitude": self.latitude,
            "longitude": self.longitude,
        }


class RentalAgreement(models.Model):
    id = models.CharField(primary_key=True, max_length=40)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="owner_rental_agreements"
    )
    tenant = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="tenant_rental_agreements"
    )
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    signed_at = models.DateTimeField(
        null=True, blank=True
    )  # The date at which the agreement is signed by the owner and tenant
    start_at = models.DateTimeField(null=True, blank=True)
    end_at = models.DateTimeField(null=True, blank=True)
    is_renewable = models.BooleanField(default=False)
    remarks = models.TextField()  # Any extra conditions to be added
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
