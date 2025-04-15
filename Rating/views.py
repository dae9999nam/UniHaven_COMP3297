from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Rating
from .serializers import RatingSerializer
from Accommodations.models import Accommodation

class AccommodationRatingDetail(APIView):
    """
    This view handles the rating for a specific accommodation (identified by its ID).
    - If no rating exists for the accommodation, a POST request creates one.
    - If a rating exists, GET retrieves it, PUT/PATCH updates it, and DELETE deletes it.
    """
    def get_object(self, accommodation_id):
        """
        Retrieve the Rating object for the given accommodation.
        If the accommodation doesn't exist, a 404 error is raised.
        If no rating exists for that accommodation, None is returned.
        """
        # Ensure the accommodation exists
        accommodation = get_object_or_404(Accommodation, pk=accommodation_id)
        try:
            return Rating.objects.get(accommodation=accommodation)
        except Rating.DoesNotExist:
            return None

    def get(self, request, accommodation, format=None):
        rating = self.get_object(accommodation)
        if rating is None:
            return Response({"detail": "Rating not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = RatingSerializer(rating)
        return Response(serializer.data)

    def post(self, request, accommodation, format=None):
        """
        Create a new rating for the specified accommodation.
        If a rating already exists for that accommodation, inform the client.
        """
        if self.get_object(accommodation) is not None:
            return Response(
                {"detail": "Rating already exists for this accommodation. Use PUT/PATCH to update."},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Copy the request data and force-set the foreign key using the accommodation ID from the URL.
        data = request.data.copy()
        data['accommodation'] = accommodation
        serializer = RatingSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, accommodation, format=None):
        """
        Update the existing rating for the given accommodation.
        """
        rating = self.get_object(accommodation)
        if rating is None:
            return Response({"detail": "Rating not found. Create one first."}, status=status.HTTP_404_NOT_FOUND)
        serializer = RatingSerializer(rating, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, accommodation, format=None):
        """
        Delete the existing rating for the given accommodation.
        """
        rating = self.get_object(accommodation)
        if rating is None:
            return Response({"detail": "Rating not found."}, status=status.HTTP_404_NOT_FOUND)
        rating.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
