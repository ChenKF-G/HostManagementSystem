"""
机房序列化器（apps/idc/serializers.py）
"""
from rest_framework import serializers

from apps.idc.models import IDC


class IDCCreateSerializer(serializers.ModelSerializer):
    """创建机房"""

    class Meta:
        model = IDC
        fields = ["id", "city", "name", "code", "address"]
        extra_kwargs = {
            "code": {"error_messages": {"unique": "机房编码已存在"}},
        }


class IDCUpdateSerializer(serializers.ModelSerializer):
    """更新机房"""

    class Meta:
        model = IDC
        fields = ["id", "city", "name", "code", "address"]
        read_only_fields = ["id"]


class IDCSerializer(serializers.ModelSerializer):
    """机房列表/详情"""

    city_name = serializers.CharField(source="city.name", read_only=True)

    class Meta:
        model = IDC
        fields = ["id", "city", "city_name", "name", "code", "address", "create_time", "update_time"]
