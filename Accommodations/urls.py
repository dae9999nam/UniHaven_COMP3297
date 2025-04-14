from django.urls import path
from . import views


urlpatterns = [
    path("Accommodations/", views.ViewAccommodation.as_view(), name="Accommodation List"),
    path("Accommodations/create", views.CreateAccommodationList.as_view(), name="Create"),
    path("Accommodations/<int:pk>", views.ModifyAccommodation.as_view(), name="Update"),
    path("Accommodations/search/", views.SearchAccommodation.as_view(),name="Search"),
    path("Accommodations/<int:pk>/distance/", views.AccommodationDistance.as_view(), name="distance"),

]