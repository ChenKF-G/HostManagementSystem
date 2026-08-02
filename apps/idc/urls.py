"""
机房路由（apps/idc/urls.py）
"""
from rest_framework.routers import DefaultRouter

from apps.idc.views import IDCViewSet

router = DefaultRouter()
router.register("idcs", IDCViewSet, basename="idc")

urlpatterns = router.urls
