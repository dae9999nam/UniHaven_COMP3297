from django.shortcuts import render
from rest_framework import generics
from .models import Accommodation
from .serializers import AccommodationSerializer
# Create your views here.

class CreateAccommodationList(generics.ListCreateAPIView):
    queryset = Accommodation.objects.all() #import all the dataset
    serializer_class = AccommodationSerializer

class ModifyAccommodation(generics.RetrieveUpdateDestroyAPIView): # To update and delete Accommodation item
    queryset = Accommodation.objects.all()
    serializer_class = AccommodationSerializer
    lookup_field = "pk"

#class DeleteAccommodationList