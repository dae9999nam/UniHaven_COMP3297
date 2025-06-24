from rest_framework import serializers
from .models import Accommodation

class AccommodationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accommodation
        fields = [ "accommodation_id", 
                  "name", 
                  "address", 
                  "type",
                  "rental_price", 
                  "rental_period", 
                  "number_of_beds",
                  "number_of_bedrooms",
                  "longitude", 
                  "latitude",
                  "GeoAddress",
                  "availability_startdate",
                  "availability_enddate", 
                  "uploaded_date"
                  ]