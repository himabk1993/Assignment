from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import (ApartmentsDetail, ApartmentsView, BuildingsDetailView,
                    BuildingsView, RentalAgreementDetailView,
                    RentalAgreementView)

urlpatterns = [
    path("apartments/", csrf_exempt(ApartmentsView.as_view()), name="apartment"),
    path(
        "apartments/<str:pk>",
        csrf_exempt(ApartmentsDetail.as_view()),
        name="apartment_details",
    ),
    path("buildings/", csrf_exempt(BuildingsView.as_view()), name="building"),
    path(
        "buildings/<str:pk>",
        csrf_exempt(BuildingsDetailView.as_view()),
        name="building_details",
    ),
    path(
        "rental_agreement/",
        csrf_exempt(RentalAgreementView.as_view()),
        name="rental_agreement",
    ),
    path(
        "rental_agreement/<str:pk>",
        csrf_exempt(RentalAgreementDetailView.as_view()),
        name="rental_agreement_details",
    ),
]
