"""
城市路由（apps/city/urls.py）
"""
from rest_framework.routers import DefaultRouter

from apps.city.views import CityViewSet

router = DefaultRouter()
router.register("cities", CityViewSet, basename="city")

urlpatterns = router.urls
