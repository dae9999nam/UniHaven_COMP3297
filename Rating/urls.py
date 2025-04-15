from django.urls import path
from .views import AccommodationRatingDetail

urlpatterns = [
    path('Accommodations/<int:accommodation>/rating/', AccommodationRatingDetail.as_view(), name='accommodation_rating'),
]