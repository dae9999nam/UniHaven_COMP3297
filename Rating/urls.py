from django.urls import path
from .views import AccommodationRatingDetail, CreateAccommodationRating

urlpatterns = [
    path('Accommodations/<int:pk>/rating/', AccommodationRatingDetail.as_view(), name='accommodation_rating'),
    path("Accommodations/<int:pk>/rating/create/", CreateAccommodationRating.as_view(), name="create_rating"),
]