"""
城市视图（apps/city/views.py）

城市 CRUD，采用 ModelViewSet。
View 层只负责参数接收 -> 调用序列化 -> 封装返回。
"""
from rest_framework import filters, viewsets

from apps.city.models import City
from apps.city.serializers import (
    CityCreateSerializer,
    CitySerializer,
    CityUpdateSerializer,
)
from services.operation_log_service import OperationLogService


class CityViewSet(viewsets.ModelViewSet):
    """
    城市管理 ViewSet
    list:     GET    /api/cities/
    create:   POST   /api/cities/
    retrieve: GET    /api/cities/{id}/
    update:   PUT    /api/cities/{id}/
    destroy:  DELETE /api/cities/{id}/
    """
    queryset = City.objects.all().order_by("-id")
    lookup_field = "id"
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "code"]
    ordering_fields = ["id", "name", "code", "create_time"]

    def get_serializer_class(self):
        if self.action == "create":
            return CityCreateSerializer
        if self.action in ["update", "partial_update"]:
            return CityUpdateSerializer
        return CitySerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        OperationLogService.record(
            self.request, "create", "city", instance.id, {"name": instance.name}
        )

    def perform_update(self, serializer):
        instance = serializer.save()
        OperationLogService.record(
            self.request, "update", "city", instance.id, {"name": instance.name}
        )

    def perform_destroy(self, instance):
        OperationLogService.record(self.request, "delete", "city", instance.id, {"name": instance.name})
        instance.delete()
