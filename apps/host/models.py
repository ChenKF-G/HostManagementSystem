"""
主机模型（apps/host/models.py）

包含：
- Host（主机表）
- HostPasswordHistory（密码历史表）

关键设计：密码单独存放于 host_password_history 表，与主机基本属性分离，
便于权限隔离、历史追溯与轮换管理。
"""
from django.db import models

from apps.common.models import TimeStampedModel
from apps.idc.models import IDC
from constants.status import HOST_STATUS_CHOICES, OFFLINE


class HostManager(models.Manager):
    """自定义 Host 管理器：封装复杂查询"""

    def online(self):
        return self.get_queryset().filter(status="online")

    def offline(self):
        return self.get_queryset().filter(status="offline")

    def by_idc(self, idc_id):
        return self.get_queryset().filter(idc_id=idc_id)

    def by_city(self, city_id):
        return self.get_queryset().filter(idc__city_id=city_id)


class Host(TimeStampedModel):
    """主机表"""

    hostname = models.CharField("主机名", max_length=100, unique=True)
    ip = models.CharField("IP 地址", max_length=45, unique=True)
    port = models.PositiveSmallIntegerField("SSH 端口", default=22)
    idc = models.ForeignKey(
        IDC, verbose_name="所属机房", on_delete=models.CASCADE, related_name="hosts"
    )
    status = models.CharField(
        "在线状态", max_length=20, choices=HOST_STATUS_CHOICES, default=OFFLINE
    )
    os_type = models.CharField("操作系统", max_length=50, null=True, blank=True)
    remark = models.CharField("备注", max_length=255, null=True, blank=True)

    objects = HostManager()

    class Meta:
        db_table = "host"
        verbose_name = "主机"
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return f"{self.hostname} ({self.ip})"


class HostPasswordHistory(models.Model):
    """密码历史表：记录每次密码轮换的加密结果与生命周期"""

    host = models.ForeignKey(
        Host,
        verbose_name="关联主机",
        on_delete=models.CASCADE,
        related_name="password_history",
    )
    encrypted_password = models.BinaryField("加密后的密码", max_length=512)
    is_active = models.BooleanField("是否当前有效", default=False)
    valid_from = models.DateTimeField("生效时间")
    expire_at = models.DateTimeField("过期时间")
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        db_table = "host_password_history"
        verbose_name = "密码历史"
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=["host", "is_active"]),
        ]

    def __str__(self):
        return f"host{self.host_id}-{'active' if self.is_active else 'inactive'}"
