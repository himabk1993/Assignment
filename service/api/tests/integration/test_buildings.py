from datetime import datetime

from http import HTTPStatus
from django.test import Client, TestCase
from django.urls import reverse

from api.models import Building, User
from api.serializers import BuildingSerializer

client = Client(raise_request_exception=False)


class BuildingTest(TestCase):
    def setUp(self):
        self.payload = {
            "name": "Test Building",
            "street": "Elsa",
            "user_id": 1,
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
        self.payload["user_id"] = int(User.objects.all()[0].id)

    def test_post_building_with_valid_user(self):
        response = client.post(
            reverse("building"), data=self.payload, content_type="application/json"
        )
        self.assertEqual(response.status_code, HTTPStatus.CREATED)

    def test_get_all_buildings(self):
        response = client.post(
            reverse("building"), data=self.payload, content_type="application/json"
        )
        response = client.get(reverse("building"))
        buildings = Building.objects.all()
        serialized_data = BuildingSerializer().dump(buildings, many=True)
        self.assertEqual(response.json(), serialized_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_get_one_building(self):
        response = client.post(
            reverse("building"), data=self.payload, content_type="application/json"
        )
        building_id = response.json()["id"]
        response = client.get(reverse("building_details", kwargs={"pk": building_id}))
        building = Building.objects.get(id=building_id)
        serialized_data = BuildingSerializer().dump(building)
        self.assertEqual(response.json(), serialized_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_update_building(self):
        response = client.post(
            reverse("building"), data=self.payload, content_type="application/json"
        )
        building = response.json()
        building_id = building.pop("id")
        building["name"] = "New Building"
        response = client.put(
            reverse("building_details", kwargs={"pk": building_id}),
            data=building,
            content_type="application/json",
        )
        building = Building.objects.get(id=building_id)
        serialized_data = BuildingSerializer().dump(building)

        self.assertEqual(response.json()["name"], serialized_data["name"])
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_delete_building(self):
        response = client.post(
            reverse("building"), data=self.payload, content_type="application/json"
        )
        building = response.json()
        response = client.delete(
            reverse("building_details", kwargs={"pk": str(building["id"])})
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_delete_not_existing_building(self):
        response = client.delete(reverse("building_details", kwargs={"pk": "6665545"}))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
