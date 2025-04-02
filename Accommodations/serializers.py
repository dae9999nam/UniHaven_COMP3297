from rest_framework import serializers
from .models import Accommodation

class AccommodationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accommodation
        fields = ["id", "location", "rental_price", "rental_period","number_of_beds","number_of_bedrooms","distance_from_campus", "availability_status", "uploaded_date"]