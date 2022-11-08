import json
import logging
from datetime import datetime

from django.http import JsonResponse
from django.views import View
from http import HTTPStatus

from .models import Apartment, Building, RentalAgreement
from .schemas import (CreateApartment, CreateBuilding, CreateRentalAgreement,
                      UpdateApartment, UpdateBuilding, UpdateRentalAgreement)
from .serializers import (ApartmentSerializer, BuildingSerializer,
                          RentalAgreementSerializer)
from .validators import BuildingValidator


logger = logging.getLogger(__name__)

class ApartmentsView(View):
    def get(self, request):
        apartments = Apartment.objects.filter(deleted_at=None)
        serialized_data = ApartmentSerializer().dump(apartments, many=True)
        return JsonResponse(serialized_data, safe=False, status=HTTPStatus.OK)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        try:
            serialized_data = CreateApartment().dump(data)
            Apartment.objects.create(**serialized_data)
            return JsonResponse(serialized_data, safe=False, status=HTTPStatus.CREATED)
        except Exception as e:
            logger.error("Couldn't create apartment due to %s" % str(e))
            return JsonResponse(
                {
                    "message": "Something went wrong! Couldn't create apartment, Please try again."
                },
                status=HTTPStatus.BAD_REQUEST,
            )


class ApartmentsDetail(View):
    def put(self, request, pk, *args, **kwargs):
        apartment = Apartment.objects.filter(id=pk)
        if apartment:
            data = json.loads(request.body)
            serialized_data = UpdateApartment().dump(data)
            apartment.update(**serialized_data)
            return JsonResponse(serialized_data, safe=False, status=HTTPStatus.OK)
        else:
            return JsonResponse(
                {
                    "message": "Something went wrong! Couldn't update apartment, Please try again."
                },
                status=HTTPStatus.NO_CONTENT,
            )

    def get(self, request, pk):
        try:
            apartment = Apartment.objects.get(id=pk)
            serialized_data = ApartmentSerializer().dump(apartment)
            return JsonResponse(serialized_data, status=HTTPStatus.OK)
        except Exception as e:
            logger.error("No such apartment is available due to %s" % str(e))
            JsonResponse(
                {
                    "message": "Something went wrong! No such apartment is available, Please try again."
                },
                status=HTTPStatus.NO_CONTENT,
            )

    def delete(self, request, pk, *args, **kwargs):
        try:
            apartment = Apartment.objects.get(id=pk)
            apartment.delete()
            return JsonResponse({"message": "The apartment is deleted!"}, status=HTTPStatus.OK)
        except Exception as e:
            logger.error("Couldn't delete apartment due to %s" % str(e))
            return JsonResponse(
                {
                    "message": "Something went wrong! Couldn't delete apartment, Please try again."
                },
                status=404,
            )


class BuildingsView(View):
    def get(self, request):
        buildings = Building.objects.filter(deleted_at=None)
        serialized_data = BuildingSerializer().dump(buildings, many=True)
        return JsonResponse(serialized_data, safe=False, status=HTTPStatus.OK)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        try:
            validated_data = BuildingValidator(**data).dict()
            Building.objects.create(**validated_data)
            return JsonResponse(validated_data, safe=False, status=HTTPStatus.CREATED)
        except ValueError as e:
            logger.error("Couldn't create building due to %s" % str(e))
        except Exception as e:
            logger.error("Couldn't create building due to %s" % str(e))
            return JsonResponse(
                {
                    "message": "Something went wrong! Couldn't create building, Please try again."
                },
                status=HTTPStatus.BAD_REQUEST,
            )


class BuildingsDetailView(View):
    def get(self, request, pk):
        try:
            building = Building.objects.get(id=pk)
            serialized_data = BuildingSerializer().dump(building)
            return JsonResponse(serialized_data, safe=False, status=HTTPStatus.OK)
        except Exception as e:
            logger.error("No such a building is available due to %s" % str(e))
            return JsonResponse(
                {
                    "message": "Something went wrong! No such a building is available, Please try again."
                },
                status=HTTPStatus.NO_CONTENT,
            )

    def put(self, request, pk, *args, **kwargs):
        building = Building.objects.filter(id=pk)
        if building:
            data = json.loads(request.body)
            serialized_data = UpdateBuilding().dump(data)
            building.update(**serialized_data)
            return JsonResponse(serialized_data, safe=False, status=HTTPStatus.OK)
        else:
            return JsonResponse(
                {
                    "message": "Something went wrong! Couldn't update the building, Please try again."
                },
                status=HTTPStatus.NO_CONTENT,
            )

    def delete(self, request, pk, *args, **kwargs):
        try:
            building = Building.objects.get(id=pk)
            building.deleted_at = datetime.now()
            building.save()
            return JsonResponse({"message": "The building is deleted"}, status=HTTPStatus.OK)
        except Exception as e:
            logger.error("Couldn't delete the building due to %s" % str(e))
            return JsonResponse(
                {
                    "message": "Something went wrong! Couldn't delete the building, Please try again."
                },
                status=404,
            )


class RentalAgreementView(View):
    def get(self, request):
        rental_agreements = RentalAgreement.objects.filter(deleted_at=None)
        serialized_data = RentalAgreementSerializer().dump(rental_agreements, many=True)
        return JsonResponse(serialized_data, safe=False, status=HTTPStatus.OK)

    def post(self, request):
        data = json.loads(request.body)
        serialized_data = CreateRentalAgreement().dump(data)
        try:
            RentalAgreement.objects.create(**serialized_data)
            return JsonResponse(serialized_data, safe=False, status=HTTPStatus.CREATED)
        except Exception as e:
            logger.error("Couldn't create the rental agreement due to %s" % str(e))
            return JsonResponse(
                {
                    "message": "Something went wrong! Couldn't create the rental agreement, Please try again."
                },
                status=HTTPStatus.BAD_REQUEST,
            )


class RentalAgreementDetailView(View):
    def get(self, request, pk):
        try:
            rental_agreement = RentalAgreement.objects.get(id=pk)
            serialized_data = RentalAgreementSerializer().dump(rental_agreement)
            return JsonResponse(serialized_data, safe=False, status=HTTPStatus.OK)
        except Exception as e:
            logger.error("Couldn't get the rental agreement due to %s" % str(e))
            return JsonResponse(
                {
                    "message": "Something went wrong! Couldn't get the rental agreement, Please try again."
                },
                status=HTTPStatus.NO_CONTENT,
            )

    def put(self, request, pk, *args, **kwargs):
        rental_agreement = RentalAgreement.objects.filter(id=pk)
        if rental_agreement:
            data = json.loads(request.body)
            serialized_data = UpdateRentalAgreement().dump(data)
            rental_agreement.update(**serialized_data)
            return JsonResponse(serialized_data, safe=False, status=HTTPStatus.OK)
        else:
            return JsonResponse(
                {
                    "message": "Something went wrong! Couldn't update the rental agreement, Please try again."
                },
                status=HTTPStatus.NO_CONTENT,
            )

    def delete(self, request, pk, *args, **kwargs):
        try:
            rental_agreement = RentalAgreement.objects.get(id=pk)
            rental_agreement.deleted_at = datetime.now()
            rental_agreement.save()
            return JsonResponse(
                {"message": "The rental agreement is deleted"}, status=HTTPStatus.OK
            )
        except Exception as e:
            logger.error("Couldn't delete the rental agreement due to %s" % str(e))
            return JsonResponse(
                {
                    "message": "Something went wrong! Couldn't delete the rental agreement, Please try again."
                },
                status=404,
            )
