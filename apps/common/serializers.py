"""
公共序列化基类（apps/common/serializers.py）
"""
from rest_framework import serializers

from apps.common.models import OperationLog


class OperationLogSerializer(serializers.ModelSerializer):
    """操作日志序列化器（只读查询用）"""

    username = serializers.CharField(source="user.username", read_only=True, default=None)

    class Meta:
        model = OperationLog
        fields = ["id", "user", "username", "action", "resource", "resource_id", "detail", "ip", "create_time"]
        read_only_fields = fields
