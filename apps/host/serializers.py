"""
主机序列化器（apps/host/serializers.py）

按场景拆分 Serializer（开发文档第六章核心要求）：
- HostCreateSerializer  创建（含 password 参与写入）
- HostUpdateSerializer  更新（不含密码，密码单独走轮换）
- HostListSerializer    列表（不返回密码）
- HostDetailSerializer  详情（不返回密码）
"""
from rest_framework import serializers

from apps.host.models import Host
from utils.validators import validate_ip, validate_port


class HostCreateSerializer(serializers.ModelSerializer):
    """创建主机：密码参与写入，IP/端口校验"""

    password = serializers.CharField(write_only=True, required=False, allow_blank=True)
    ip = serializers.CharField(max_length=45, validators=[validate_ip])
    port = serializers.IntegerField(default=22, validators=[validate_port])

    class Meta:
        model = Host
        fields = ["id", "hostname", "ip", "port", "idc", "password", "os_type", "remark"]
        extra_kwargs = {
            "hostname": {"error_messages": {"unique": "主机名已存在"}},
            "ip": {"error_messages": {"unique": "IP 地址已存在"}},
        }


class HostUpdateSerializer(serializers.ModelSerializer):
    """更新主机：不含密码字段"""

    ip = serializers.CharField(max_length=45, required=False, validators=[validate_ip])

    class Meta:
        model = Host
        fields = ["id", "hostname", "ip", "idc", "os_type", "remark"]
        read_only_fields = ["id"]


class HostListSerializer(serializers.ModelSerializer):
    """主机列表：不返回密码，含城市信息"""

    city = serializers.IntegerField(source="idc.city_id", read_only=True)
    city_name = serializers.CharField(source="idc.city.name", read_only=True)
    idc_name = serializers.CharField(source="idc.name", read_only=True)

    class Meta:
        model = Host
        fields = ["id", "hostname", "ip", "city", "city_name", "idc", "idc_name", "status", "create_time"]


class HostDetailSerializer(serializers.ModelSerializer):
    """主机详情：不返回密码"""

    city = serializers.IntegerField(source="idc.city_id", read_only=True)
    city_name = serializers.CharField(source="idc.city.name", read_only=True)
    idc_name = serializers.CharField(source="idc.name", read_only=True)

    class Meta:
        model = Host
        fields = [
            "id", "hostname", "ip", "port", "idc", "idc_name",
            "city", "city_name", "status", "os_type", "remark",
            "create_time", "update_time",
        ]


class PasswordHistorySerializer(serializers.Serializer):
    """密码历史（脱敏展示）"""

    id = serializers.IntegerField()
    masked_encrypted = serializers.CharField()
    is_active = serializers.BooleanField()
    valid_from = serializers.DateTimeField()
    expire_at = serializers.DateTimeField()
