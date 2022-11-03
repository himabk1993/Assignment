import copy
from datetime import datetime

from django.http import JsonResponse, Http404
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Apartment, Building, RentalAgreement

from .serializers import (
    ApartmentSerializer,
    BuildingSerializer,
    RentalAgreementSerializer,
)
from .schemas import (
    CreateApartment,
    UpdateApartment,
    CreateBuilding,
    UpdateBuilding,
    CreateRentalAgreement,
    UpdateRentalAgreement,
)


class ApartmentsView(APIView):
    def get(self, request):
        apartments = Apartment.objects.all()
        serializer = ApartmentSerializer(apartments, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = CreateApartment(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            Apartment.objects.create(**serializer.data)
            return Response(serializer.data, status=201)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=400)


class ApartmentsDetail(APIView):
    def put(self, request, pk, *args, **kwargs):
        apartment = Apartment.objects.filter(id=pk)
        if apartment:
            serializer = UpdateApartment(data=request.data)
            serializer.is_valid(raise_exception=True)
            apartment.update(**serializer.data)
            return Response(serializer.data, status=200)
        else:
            return JsonResponse({"message": "no content"}, status=204)

    def get(self, request, pk):
        try:
            apartment = Apartment.objects.get(id=pk)
            serializer = ApartmentSerializer(apartment)
            return JsonResponse(serializer.data, status=200)
        except Apartment.DoesNotExist:
            raise Http404

    def delete(self, request, pk, *args, **kwargs):
        try:
            apartment = Apartment.objects.get(id=pk)
            apartment.delete()
            return JsonResponse({"message": "record is deleted"}, status=200)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=404)


class BuildingsView(APIView):
    def get(self, request):
        buildings = Building.objects.filter(deleted_at=None)
        serializer = BuildingSerializer(buildings, many=True)
        return JsonResponse(serializer.data, safe=False, status=200)

    def post(self, request, *args, **kwargs):
        serializer = CreateBuilding(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            Building.objects.create(**serializer.data)
            return JsonResponse(serializer.data, safe=False, status=201)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=400)


class BuildingsDetailView(APIView):
    def get(self, request, pk):
        try:
            building = Building.objects.get(id=pk)
            serializer = BuildingSerializer(building)
            return JsonResponse(serializer.data, safe=False, status=200)
        except Building.DoesNotExist:
            return JsonResponse(
                {"message": "No such a building is available"}, status=204
            )

    def put(self, request, pk, *args, **kwargs):
        building = Building.objects.filter(id=pk)
        if building:
            serializer = UpdateBuilding(data=request.data)
            serializer.is_valid(raise_exception=True)
            building.update(**serializer.data)
            return JsonResponse(serializer.data, safe=False, status=200)
        else:
            return JsonResponse({"message": "Couldn't update the building"}, status=204)

    def delete(self, request, pk, *args, **kwargs):
        try:
            building = Building.objects.get(id=pk)
            building.deleted_at = datetime.now()
            building.save()
            return JsonResponse({"message": "Record is deleted"}, status=200)
        except Exception:
            return JsonResponse({"message": "Couldn't delete the record"}, status=404)


class RentalAgreementView(APIView):
    def get(self, request):
        rental_agreements = RentalAgreement.objects.all()
        serializer = RentalAgreementSerializer(rental_agreements, many=True)
        return JsonResponse(serializer.data, safe=False, status=200)

    def post(self, request):
        serializer = CreateRentalAgreement(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            data = copy.copy(serializer.data)
            RentalAgreement.objects.create(**data)
            return JsonResponse(serializer.data, safe=False, status=201)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=400)


class RentalAgreementDetailView(APIView):
    def get(self, request, pk):
        try:
            rental_agreement = RentalAgreement.objects.get(id=pk)
            serializer = RentalAgreementSerializer(rental_agreement)
            return JsonResponse(serializer.data, safe=False, status=200)
        except Exception:
            return JsonResponse(
                {"message": "No such a building is available"}, status=204
            )

    def put(self, request, pk, *args, **kwargs):
        rental_agreement = RentalAgreement.objects.filter(id=pk)
        if rental_agreement:
            serializer = UpdateRentalAgreement(data=request.data)
            serializer.is_valid(raise_exception=True)
            rental_agreement.update(**serializer.data)
            return JsonResponse(serializer.data, safe=False, status=200)
        else:
            return JsonResponse({"message": "Couldn't update the building"}, status=204)

    def delete(self, request, pk, *args, **kwargs):
        try:
            rental_agreement = RentalAgreement.objects.get(id=pk)
            rental_agreement.deleted_at = datetime.now()
            rental_agreement.save()
            return JsonResponse({"message": "Record is deleted"}, status=200)
        except Exception:
            return JsonResponse({"message": "Couldn't delete the record"}, status=404)
