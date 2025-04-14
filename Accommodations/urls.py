from django.urls import path
from . import views


urlpatterns = [
    path("", views.ViewAccommodation.as_view(), name="Accommodation List"),
    path("create/", views.CreateAccommodationList.as_view(), name="Create"),
    path("<int:pk>/", views.ModifyAccommodation.as_view(), name="Update"),
    path("search/", views.SearchAccommodation.as_view(),name="Search"),
    path("<int:pk>/distance/", views.AccommodationDistance.as_view(), name="distance"),

]