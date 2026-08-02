"""
城市序列化器（apps/city/serializers.py）

按场景拆分：创建、更新、列表/详情。
"""
from rest_framework import serializers

from apps.city.models import City


class CityCreateSerializer(serializers.ModelSerializer):
    """创建城市"""

    class Meta:
        model = City
        fields = ["id", "name", "code", "remark"]
        extra_kwargs = {
            "name": {"error_messages": {"unique": "城市名称已存在"}},
            "code": {"error_messages": {"unique": "城市编码已存在"}},
        }


class CityUpdateSerializer(serializers.ModelSerializer):
    """更新城市"""

    class Meta:
        model = City
        fields = ["id", "name", "code", "remark"]
        read_only_fields = ["id"]


class CitySerializer(serializers.ModelSerializer):
    """城市列表/详情（公共返回）"""

    class Meta:
        model = City
        fields = ["id", "name", "code", "remark", "create_time", "update_time"]
