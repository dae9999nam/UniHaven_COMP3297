from django.urls import path
from . import views


urlpatterns = [
    path("Reservations/", views.ViewReservationList.as_view(), name="Reservation List"),
    path("Reservations/create", views.CreateReservation.as_view(), name="Create Reservation"),
    path("Reservations/modify/<int:pk>", views.ModifyReservation.as_view(), name="Modify Reservation"),
    path("Reservations/cancel/<int:pk>", views.CancelReservation.as_view(),name="Cancel Reservation"),
    path("Reservations/viewAccommodation/<int:pk>", views.ViewReservedAccommodationDetail.as_view(),name="View Reserved Accommodation Details"),

]