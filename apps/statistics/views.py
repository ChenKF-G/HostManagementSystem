"""
统计与请求日志视图（apps/statistics/views.py）

- StatisticsViewSet：统计查询（按维度/日期筛选）+ 手动触发
- RequestLogViewSet：请求耗时记录查询（只读）
"""
from django_filters import rest_framework as django_filters
from rest_framework import decorators, filters, response, status, viewsets

from apps.statistics.models import HostStatistics, RequestLog
from apps.statistics.serializers import (
    HostStatisticsSerializer,
    RequestLogSerializer,
)
from services.statistics_service import StatisticsService
from utils.response import Result


class StatisticsFilter(django_filters.FilterSet):
    """统计查询过滤器：按维度/日期筛选"""

    dimension = django_filters.CharFilter(field_name="dimension")
    date = django_filters.DateFilter(field_name="stat_date")
    start_date = django_filters.DateFilter(field_name="stat_date", lookup_expr="gte")
    end_date = django_filters.DateFilter(field_name="stat_date", lookup_expr="lte")

    class Meta:
        model = HostStatistics
        fields = ["dimension", "city", "idc", "date", "start_date", "end_date"]


class StatisticsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    统计查询 ViewSet
    list: GET /api/statistics/         统计结果列表
    run:  POST /api/statistics/run/    手动触发一次统计
    """
    queryset = HostStatistics.objects.select_related("city", "idc").all().order_by("-stat_date", "-id")
    serializer_class = HostStatisticsSerializer
    filter_backends = [django_filters.DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = StatisticsFilter
    ordering_fields = ["stat_date", "total_count", "online_count", "offline_count"]

    @decorators.action(detail=False, methods=["post"])
    def run(self, request):
        """手动触发一次统计（便于测试）"""
        result = StatisticsService.generate_statistics()
        return response.Response(
            Result.success(data=result, message="统计触发完成"),
            status=status.HTTP_200_OK,
        )


class RequestLogFilter(django_filters.FilterSet):
    """请求耗时记录过滤器"""

    method = django_filters.CharFilter(field_name="method")
    path = django_filters.CharFilter(field_name="path", lookup_expr="icontains")
    status = django_filters.NumberFilter(field_name="status")
    min_cost_ms = django_filters.NumberFilter(field_name="cost_ms", lookup_expr="gte")
    start_time = django_filters.DateTimeFilter(field_name="create_time", lookup_expr="gte")
    end_time = django_filters.DateTimeFilter(field_name="create_time", lookup_expr="lte")

    class Meta:
        model = RequestLog
        fields = ["method", "path", "status", "min_cost_ms", "start_time", "end_time"]


class RequestLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    请求耗时记录 ViewSet（只读）
    list: GET /api/request-logs/
    """
    queryset = RequestLog.objects.select_related("user").all().order_by("-create_time")
    serializer_class = RequestLogSerializer
    filter_backends = [django_filters.DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = RequestLogFilter
    ordering_fields = ["create_time", "cost_ms"]
