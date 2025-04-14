from rest_framework.routers import DefaultRouter
from .views import RatingViewSet

router = DefaultRouter()
router.register(r'ratings', RatingViewSet, basename='rating')

urlpatterns = router.urls