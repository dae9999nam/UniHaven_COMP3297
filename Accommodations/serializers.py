from rest_framework import serializers
from .models import Accommodation

class AccommodationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accommodation
        fields = [ "accommodation_id", 
                  "name", 
                  "address", 
                  "rental_price", 
                  "rental_period", 
                  "number_of_beds",
                  "number_of_bedrooms",
                  "longitude", 
                  "latitude", 
                  "availability_status", 
                  "uploaded_date"]
        # id not automatically implemented ?
        #distance from HKU is changed to longitude and latitude of the building