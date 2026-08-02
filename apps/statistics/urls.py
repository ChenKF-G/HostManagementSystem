"""
统计路由（apps/statistics/urls.py）
"""
from rest_framework.routers import DefaultRouter

from apps.statistics.views import StatisticsViewSet

router = DefaultRouter()
router.register("statistics", StatisticsViewSet, basename="statistics")

urlpatterns = router.urls
