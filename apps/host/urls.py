"""
主机路由（apps/host/urls.py）
"""
from rest_framework.routers import DefaultRouter

from apps.host.views import HostViewSet

router = DefaultRouter()
router.register("hosts", HostViewSet, basename="host")

urlpatterns = router.urls
