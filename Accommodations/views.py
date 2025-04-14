from django.shortcuts import render
from rest_framework import generics, status
from .models import Accommodation, HKU_campus_premises
from .models import equirectangular_distance # for Distance Calculation functions
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
class AccommodationDistance(APIView):
    """
    This view calculates the distance between an existing Accommodation instance
    (identified by its primary key) and a target destination selected from a predefined enum.
    
    Query Parameters:
      - destination: The target destination choice (i.e. "Main_Campus", "Sasson", "Swire", "Kadoorie_Centre", "Faculty of Dentistry")
    
    URL Parameter:
      - pk: The primary key of the Accommodation instance
    """
    def get(self, request, pk, format=None):

        # Get the "destination" query parameter
        destination_choice = request.query_params.get("destination")
        if not destination_choice:
            return Response(
                {"error": "Query parameter 'destination' is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Retrieve the Accommodation instance from the database
        try:
            accommodation = Accommodation.objects.get(pk=pk)
        except Accommodation.DoesNotExist:
            return Response(
                {"error": "Accommodation not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        # Validate and get the target destination from the enum.
        # We assume that enum keys are uppercase.
        try:
            destination = HKU_campus_premises[destination_choice.upper()]
        except KeyError:
            valid_destinations = [d.name for d in HKU_campus_premises]
            return Response(
                {"error": f"Invalid destination. Valid options are: {', '.join(valid_destinations)}."},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Unpack the destination's details (Display Name, lat, lon)
        dest_name, dest_lat, dest_lon = destination.value
        
        # Retrieve the accommodation's stored coordinates
        accom_lat = accommodation.latitude
        accom_lon = accommodation.longitude
        
        # Calculate the distance using the equirectangular approximation.
        distance = equirectangular_distance(accom_lat, accom_lon, dest_lat, dest_lon)
        
        # Return a JSON response with the computed distance and additional details.
        return Response({
            "accommodation_id": pk,
            "accommodation_coordinates": {"latitude": accom_lat, "longitude": accom_lon},
            "destination": dest_name,
            "destination_coordinates": {"latitude": dest_lat, "longitude": dest_lon},
            "distance_meters": distance
        }, status=status.HTTP_200_OK)