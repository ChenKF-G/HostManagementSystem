"""
机房视图（apps/idc/views.py）

机房 CRUD，采用 ModelViewSet。
"""
from rest_framework import filters, viewsets

from apps.idc.models import IDC
from apps.idc.serializers import IDCCreateSerializer, IDCSerializer, IDCUpdateSerializer
from services.operation_log_service import OperationLogService


class IDCViewSet(viewsets.ModelViewSet):
    """
    机房管理 ViewSet
    list:     GET    /api/idcs/
    create:   POST   /api/idcs/
    retrieve: GET    /api/idcs/{id}/
    update:   PUT    /api/idcs/{id}/
    destroy:  DELETE /api/idcs/{id}/
    """
    queryset = IDC.objects.select_related("city").all().order_by("-id")
    lookup_field = "id"
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "code", "address"]
    ordering_fields = ["id", "name", "code", "create_time"]

    def get_serializer_class(self):
        if self.action == "create":
            return IDCCreateSerializer
        if self.action in ["update", "partial_update"]:
            return IDCUpdateSerializer
        return IDCSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        OperationLogService.record(
            self.request, "create", "idc", instance.id, {"name": instance.name}
        )

    def perform_update(self, serializer):
        instance = serializer.save()
        OperationLogService.record(
            self.request, "update", "idc", instance.id, {"name": instance.name}
        )

    def perform_destroy(self, instance):
        OperationLogService.record(self.request, "delete", "idc", instance.id, {"name": instance.name})
        instance.delete()
