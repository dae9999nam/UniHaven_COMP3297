from django.shortcuts import render
from rest_framework import generics, status, viewsets, mixins
from .models import Accommodation
from .serializers import AccommodationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

#Create Accommodatioin Items
class CreateAccommodationList(generics.ListCreateAPIView):
    queryset = Accommodation.objects.all() #import all the dataset
    serializer_class = AccommodationSerializer
    
#Modify and Delete Accomodation Items
class ModifyAccommodation(generics.RetrieveUpdateDestroyAPIView): # To update and delete Accommodation item
    queryset = Accommodation.objects.all()
    serializer_class = AccommodationSerializer
    lookup_field = "pk"

#View Accommodation Item
class ViewAccommodation(generics.ListAPIView):
    queryset = Accommodation.objects.all()
    serializer_class = AccommodationSerializer

class SearchAccommodation(APIView):
    def get(self, request, format=None):
        #Get the name of building from the query parameter default as empty string 
        name = request.query_params.get("name", None)
        if name:
            #Filter the queryset based on the accommodation name
            accommodation = Accommodation.objects.filter(name__icontains=name)
        else:
            #If no building name is provided, return all accommodation items
            accommodation = Accommodation.objects.all()
        serializer = AccommodationSerializer(accommodation, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# We want to calculate distance for one specific accommodation 
# Choose which HKU campus or premises to measure distance
'''class CalculateDistance(APIView):
    query = Accommodation.objects.filter(id__icontains=accommodation_id)
    long = query.longitude
    lat = query.latitude
    # Which compus object to choose
    # Calculate distance - since distances are small, there is no need to calculate them as great-circle distances; line of sight distances are sufficient
    equirectangular projection
    # Show the result
    serializer_class = AccommodationSerializer'''

