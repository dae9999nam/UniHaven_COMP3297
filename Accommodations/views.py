from django.shortcuts import render
from rest_framework import generics, status, viewsets
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
        name = request.query_params.get("Building Name", "")
        if name:
            #Filter the queryset based on the accommodation name
            accommodation = Accommodation.objects.filter(name_icontains=name)
        else:
            #If no building name is provided, return all accommodation items
            accommodation = Accommodation.objects.all()
        serializer = AccommodationSerializer(accommodation, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)