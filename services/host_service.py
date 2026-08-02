"""
主机业务服务（services/host_service.py）

负责主机创建、更新、删除、查询等核心业务逻辑。
View 层调用本服务，Model 层只做持久化。
"""
import logging

from django.db import transaction

from apps.host.models import Host, HostPasswordHistory

logger = logging.getLogger("app")


class HostService:
    @staticmethod
    def create_host(validated_data) -> Host:
        """
        创建主机，并加密存储初始 root 密码。
        validated_data 中可含 password（明文），由调用方先剥离非模型字段。
        """
        password = validated_data.pop("password", None)
        with transaction.atomic():
            host = Host.objects.create(**validated_data)
            if password:
                from services.password_service import PasswordService

                PasswordService.store_password(host, password)
        logger.info(f"创建主机成功: {host.hostname} ({host.ip})")
        return host

    @staticmethod
    def update_host(host, validated_data) -> Host:
        """更新主机基本属性（不含密码）"""
        for field, value in validated_data.items():
            setattr(host, field, value)
        host.save()
        logger.info(f"更新主机成功: id={host.id}")
        return host

    @staticmethod
    def delete_host(host) -> None:
        """删除主机（级联删除密码历史由 signal 处理）"""
        host_id = host.id
        host.delete()
        logger.info(f"删除主机成功: id={host_id}")

    @staticmethod
    def list_hosts(queryset=None, **filters):
        """查询主机列表，支持按 idc / city / status / keyword 过滤"""
        if queryset is None:
            queryset = Host.objects.select_related("idc__city").all()
        return queryset
