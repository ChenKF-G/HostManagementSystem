"""
请求日志路由（apps/statistics/request_log_urls.py）
"""
from rest_framework.routers import DefaultRouter

from apps.statistics.views import RequestLogViewSet

router = DefaultRouter()
router.register("request-logs", RequestLogViewSet, basename="request-log")

urlpatterns = router.urls
