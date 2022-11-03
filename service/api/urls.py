from django.urls import path

from .views import (
    ApartmentsView,
    ApartmentsDetail,
    BuildingsView,
    BuildingsDetailView,
    RentalAgreementView,
    RentalAgreementDetailView,
)


urlpatterns = [
    path("apartments/", ApartmentsView.as_view(), name="apartment"),
    path("apartments/<str:pk>", ApartmentsDetail.as_view(), name="apartment_details"),
    path("buildings/", BuildingsView.as_view(), name="building"),
    path("buildings/<str:pk>", BuildingsDetailView.as_view(), name="building_details"),
    path("rental_agreement/", RentalAgreementView.as_view(), name="rental_agreement"),
    path(
        "rental_agreement/<str:pk>",
        RentalAgreementDetailView.as_view(),
        name="rental_agreement_details",
    ),
]
