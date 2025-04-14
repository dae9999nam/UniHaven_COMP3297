from rest_framework import viewsets
from .models import Rating
from .serializers import RatingSerializer

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all().order_by('-uploaded_date')
    serializer_class = RatingSerializer