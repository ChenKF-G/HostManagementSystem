"""
主机视图（apps/host/views.py）

主机 CRUD + 自定义 action：
- POST /api/hosts/{id}/ping/        探测主机可达性
- GET  /api/hosts/{id}/passwords/   查看密码历史（脱敏）

View 层遵循：参数接收 -> 调用 Service -> 封装返回。
"""
from rest_framework import decorators, filters, response, status, viewsets

from apps.host.models import Host
from apps.host.serializers import (
    HostCreateSerializer,
    HostDetailSerializer,
    HostListSerializer,
    HostUpdateSerializer,
    PasswordHistorySerializer,
)
from services.host_service import HostService
from services.operation_log_service import OperationLogService
from services.password_service import PasswordService
from services.ping_service import PingService
from utils.response import Result


class HostViewSet(viewsets.ModelViewSet):
    """
    主机管理 ViewSet
    list:      GET    /api/hosts/
    create:    POST   /api/hosts/
    retrieve:  GET    /api/hosts/{id}/
    update:    PUT    /api/hosts/{id}/
    destroy:   DELETE /api/hosts/{id}/
    ping:      POST   /api/hosts/{id}/ping/
    passwords: GET    /api/hosts/{id}/passwords/
    """
    queryset = Host.objects.select_related("idc__city").all()
    lookup_field = "id"
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["hostname", "ip", "os_type", "idc__name"]
    ordering_fields = ["id", "hostname", "ip", "status", "create_time"]

    def get_serializer_class(self):
        if self.action == "create":
            return HostCreateSerializer
        if self.action in ["update", "partial_update"]:
            return HostUpdateSerializer
        if self.action == "retrieve":
            return HostDetailSerializer
        return HostListSerializer

    def create(self, request, *args, **kwargs):
        """创建主机：调用 HostService.create_host 处理密码加密"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        host = HostService.create_host(serializer.validated_data)
        OperationLogService.record(
            request, "create", "host", host.id, {"hostname": host.hostname, "ip": host.ip}
        )
        return response.Response(
            Result.success(data=HostDetailSerializer(host).data, message="创建成功"),
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        """更新主机：调用 HostService.update_host"""
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        host = HostService.update_host(instance, serializer.validated_data)
        OperationLogService.record(
            request, "update", "host", host.id, {"hostname": host.hostname}
        )
        return response.Response(Result.success(data=HostDetailSerializer(host).data))

    def destroy(self, request, *args, **kwargs):
        """删除主机"""
        instance = self.get_object()
        OperationLogService.record(
            request, "delete", "host", instance.id, {"hostname": instance.hostname}
        )
        HostService.delete_host(instance)
        return response.Response(Result.success(data=None, message="删除成功"),
                                status=status.HTTP_204_NO_CONTENT)

    @decorators.action(detail=True, methods=["post"])
    def ping(self, request, id=None):
        """探测指定主机 ping 可达性"""
        host = self.get_object()
        online = PingService.ping_host(host)
        return response.Response(
            Result.success(
                data={"id": host.id, "hostname": host.hostname, "ip": host.ip, "status": host.status},
                message="ping 探测完成",
            )
        )

    @decorators.action(detail=True, methods=["get"])
    def passwords(self, request, id=None):
        """查看指定主机密码历史（脱敏展示）"""
        host = self.get_object()
        history = PasswordService.get_history(host, masked=True)
        return response.Response(
            Result.success(data=PasswordHistorySerializer(history, many=True).data)
        )
