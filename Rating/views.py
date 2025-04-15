from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from django.shortcuts import get_object_or_404
from Accommodations.models import Accommodation  # Make sure this import reflects your project structure
from Rating.models import Rating
from Rating.serializers import RatingSerializer

class AccommodationRatingDetail(APIView):
    """
    View, update, or delete the rating for a specified accommodation.
    URL: /Accommodations/<int:pk>/rating/
    """

    def get_object(self, accommodation_id):
        accommodation = get_object_or_404(Accommodation, pk=accommodation_id)
        try:
            # Attempt to get the rating linked to this accommodation.
            return Rating.objects.get(accommodation=accommodation)
        except Rating.DoesNotExist:
            return None

    def get(self, request, pk, format=None):
        rating = self.get_object(pk)
        if rating is None:
            return Response({"detail": "Rating not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = RatingSerializer(rating)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        rating = self.get_object(pk)
        if rating is None:
            return Response({"detail": "Rating not found. Create one first."}, status=status.HTTP_404_NOT_FOUND)
        serializer = RatingSerializer(rating, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # You may also implement patch if you prefer partial updates.
    def patch(self, request, pk, format=None):
        rating = self.get_object(pk)
        if rating is None:
            return Response({"detail": "Rating not found. Create one first."}, status=status.HTTP_404_NOT_FOUND)
        serializer = RatingSerializer(rating, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        rating = self.get_object(pk)
        if rating is None:
            return Response({"detail": "Rating not found."}, status=status.HTTP_404_NOT_FOUND)
        rating.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CreateAccommodationRating(generics.CreateAPIView):
    serializer_class = RatingSerializer

    def perform_create(self, serializer):
        # Retrieve the accommodation ID from the URL, then set it automatically
        acc_pk = self.kwargs.get('pk')
        accommodation = get_object_or_404(Accommodation, pk=acc_pk)
        serializer.save(accommodation=accommodation)

"""
class CreateAccommodationRating(APIView):
 
    Create a new rating for a specified accommodation.
    URL: /Accommodations/<int:pk>/rating/create/
   
    def post(self, request, pk, format=None):
        accommodation = get_object_or_404(Accommodation, pk=pk)
        # Check if a rating already exists for this accommodation.
        try:
            Rating.objects.get(accommodation=accommodation)
            return Response({"detail": "Rating already exists for this accommodation. Cannot make more than 1"},
                            status=status.HTTP_400_BAD_REQUEST)
        except Rating.DoesNotExist:
            pass

        data = request.data.copy()
        data['accommodation'] = pk  # Set the foreign key automatically using the URL parameter.
        serializer = RatingSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
"""