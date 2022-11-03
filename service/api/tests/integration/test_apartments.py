from datetime import datetime

from rest_framework import status
from django.urls import reverse
from django.test import TestCase, Client
from api.models import Apartment, User
from api.serializers import ApartmentSerializer

client = Client()


class ApartmentTest(TestCase):
    def setUp(self):
        self.payload = {
            "rent": 7938,
            "area": 77,
            "description": "",
            "latitude": "59.3681439",
            "rooms": 3,
            "longitude": "16.4986661",
            "floor": 0,
        }

        building_payload = {
            "name": "Test Building",
            "street": "Elsa",
            "user_id": "1",
            "city": "Kannur",
            "number": 90,
            "street_number": "57",
            "association_name": "BRF Kannur new",
        }

        user_payload = {
            "full_name": "Tester",
            "identity_number": "1001",
            "email": "test@gmail.com",
            "license_until": datetime.now(),
        }

        User.objects.create(**user_payload)
        self.payload["user_id"] = str(User.objects.all()[0].id)
        building_payload["user_id"] = str(User.objects.all()[0].id)
        response = client.post(
            reverse("building"), data=building_payload, content_type="application/json"
        )
        self.payload["building_id"] = str(response.json()["id"])

    def test_post_apartment_with_valid_user(self):
        response = client.post(
            reverse("apartment"), data=self.payload, content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_all_buildings(self):
        response = client.post(
            reverse("apartment"), data=self.payload, content_type="application/json"
        )
        response = client.get(reverse("apartment"))
        apartments = Apartment.objects.all()
        ApartmentSerializer(apartments, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_one_apartment(self):
        response = client.post(
            reverse("apartment"), data=self.payload, content_type="application/json"
        )
        aprtment_id = response.json()["id"]
        response = client.get(reverse("apartment_details", kwargs={"pk": aprtment_id}))
        aprtment = Apartment.objects.get(id=aprtment_id)
        serializer = ApartmentSerializer(aprtment)
        self.assertEqual(response.json(), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_apartment(self):
        response = client.post(
            reverse("apartment"), data=self.payload, content_type="application/json"
        )
        apartment = response.json()
        apartment_id = apartment.pop("id")
        apartment["rooms"] = 9
        response = client.put(
            reverse("apartment_details", kwargs={"pk": apartment_id}),
            data=apartment,
            content_type="application/json",
        )
        apartment = Apartment.objects.get(id=apartment_id)
        serializer = ApartmentSerializer(apartment, only=("rooms",))
        self.assertEqual(response.json()["rooms"], serializer.data["rooms"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_apartment(self):
        response = client.post(
            reverse("apartment"), data=self.payload, content_type="application/json"
        )
        apartment = response.json()
        response = client.delete(
            reverse("apartment_details", kwargs={"pk": str(apartment["id"])})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
