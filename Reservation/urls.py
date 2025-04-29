from django.urls import path
from . import views


urlpatterns = [
    path("reservations/", views.ViewReservationList.as_view(), name="Reservation List"),
    path("reservations/create", views.CreateReservation.as_view(), name="Create Reservation"),
    path("reservations/modify/<int:pk>", views.ModifyReservation.as_view(), name="Modify Reservation"),
    path("reservations/cancel/<int:pk>", views.CancelReservation.as_view(),name="Cancel Reservation"),
    path("reservations/<int:pk>/accommodation", views.ViewReservedAccommodationDetail.as_view(),name="View Reserved Accommodation Details"),
]