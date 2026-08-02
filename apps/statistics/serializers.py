"""
统计与请求日志序列化器（apps/statistics/serializers.py）
"""
from rest_framework import serializers

from apps.statistics.models import HostStatistics, RequestLog


class HostStatisticsSerializer(serializers.ModelSerializer):
    """主机统计序列化器"""

    city_name = serializers.CharField(source="city.name", read_only=True)
    idc_name = serializers.CharField(source="idc.name", read_only=True)

    class Meta:
        model = HostStatistics
        fields = [
            "id", "dimension", "city", "city_name", "idc", "idc_name",
            "total_count", "online_count", "offline_count", "stat_date", "create_time",
        ]


class RequestLogSerializer(serializers.ModelSerializer):
    """请求耗时记录序列化器（只读）"""

    username = serializers.CharField(source="user.username", read_only=True, default=None)

    class Meta:
        model = RequestLog
        fields = ["id", "user", "username", "method", "path", "status", "ip", "cost_ms", "create_time"]
        read_only_fields = fields
