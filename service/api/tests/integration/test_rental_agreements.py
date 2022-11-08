from datetime import datetime
from http import HTTPStatus

from api.models import RentalAgreement, User
from api.serializers import RentalAgreementSerializer
from django.test import Client, TestCase
from django.urls import reverse

client = Client()


class RentalAgreementTest(TestCase):
    def setUp(self):
        self.payload = {
            "is_renewable": True,
            "start_at": "2022-11-03 05:31:20.007786+01",
            "signed_at": "2022-11-01 05:31:20.007786+01",
            "end_at": "2022-11-11 05:31:20.007786+01",
        }

        apartment_payload = {
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
        self.payload["tenant_id"] = int(User.objects.all()[0].id)
        self.payload["owner_id"] = int(User.objects.all()[0].id)
        building_payload["user_id"] = int(User.objects.all()[0].id)
        response = client.post(
            reverse("building"), data=building_payload, content_type="application/json"
        )
        building_payload["building_id"] = str(response.json()["id"])
        self.payload["building_id"] = str(response.json()["id"])
        response = client.post(
            reverse("apartment"),
            data=apartment_payload,
            content_type="application/json",
        )
        self.payload["apartment_id"] = str(response.json()["id"])

    def test_post_apartment_with_valid_user(self):
        response = client.post(
            reverse("rental_agreement"),
            data=self.payload,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, HTTPStatus.CREATED)

    def test_get_all_buildings(self):
        response = client.post(
            reverse("rental_agreement"),
            data=self.payload,
            content_type="application/json",
        )
        response = client.get(reverse("rental_agreement"))
        rental_agreement = RentalAgreement.objects.all()
        RentalAgreementSerializer().dump(rental_agreement, many=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_get_one_apartment(self):
        response = client.post(
            reverse("rental_agreement"),
            data=self.payload,
            content_type="application/json",
        )
        rental_agreement_id = response.json()["id"]
        response = client.get(
            reverse("rental_agreement_details", kwargs={"pk": rental_agreement_id})
        )
        rental_agreement = RentalAgreement.objects.get(id=rental_agreement_id)
        serialized_data = RentalAgreementSerializer().dump(rental_agreement)
        self.assertEqual(response.json(), serialized_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_update_apartment(self):
        response = client.post(
            reverse("rental_agreement"),
            data=self.payload,
            content_type="application/json",
        )
        rental_agreement = response.json()
        rental_agreement_id = rental_agreement.pop("id")
        rental_agreement["is_renewable"] = False
        response = client.put(
            reverse("rental_agreement_details", kwargs={"pk": rental_agreement_id}),
            data=rental_agreement,
            content_type="application/json",
        )
        rental_agreement = RentalAgreement.objects.get(id=rental_agreement_id)
        serialized_data = RentalAgreementSerializer().dump(rental_agreement)
        self.assertEqual(
            response.json()["is_renewable"], serialized_data["is_renewable"]
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_delete_apartment(self):
        response = client.post(
            reverse("rental_agreement"),
            data=self.payload,
            content_type="application/json",
        )
        rental_agreement = response.json()
        response = client.delete(
            reverse(
                "rental_agreement_details", kwargs={"pk": str(rental_agreement["id"])}
            )
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
