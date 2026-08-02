"""
统计与请求日志模型（apps/statistics/models.py）

- HostStatistics：主机统计表（每日按城市/机房维度落库）
- RequestLog：API 请求耗时记录表
"""
from django.conf import settings
from django.db import models

from apps.city.models import City
from apps.idc.models import IDC


class HostStatistics(models.Model):
    """主机统计表"""

    DIMENSION_CHOICES = [
        ("city", "按城市"),
        ("idc", "按机房"),
    ]

    dimension = models.CharField("统计维度", max_length=20, choices=DIMENSION_CHOICES)
    city = models.ForeignKey(
        City, verbose_name="城市", on_delete=models.CASCADE, null=True, blank=True, related_name="statistics"
    )
    idc = models.ForeignKey(
        IDC, verbose_name="机房", on_delete=models.CASCADE, null=True, blank=True, related_name="statistics"
    )
    total_count = models.IntegerField("主机总数")
    online_count = models.IntegerField("在线主机数", default=0)
    offline_count = models.IntegerField("离线主机数", default=0)
    stat_date = models.DateField("统计日期")
    create_time = models.DateTimeField("写入时间", auto_now_add=True)

    class Meta:
        db_table = "host_statistics"
        verbose_name = "主机统计"
        verbose_name_plural = verbose_name
        constraints = [
            models.UniqueConstraint(
                fields=["dimension", "city", "idc", "stat_date"],
                name="uniq_stat_dimension_city_idc_date",
            )
        ]

    def __str__(self):
        target = self.city.name if self.city else (self.idc.name if self.idc else "")
        return f"{self.dimension}-{target}-{self.stat_date}"


class RequestLog(models.Model):
    """API 请求耗时记录表"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="用户",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column="user",
    )
    method = models.CharField("请求方法", max_length=10)
    path = models.CharField("请求路径", max_length=255)
    status = models.IntegerField("响应状态码")
    ip = models.CharField("客户端 IP", max_length=45, null=True, blank=True)
    cost_ms = models.DecimalField("处理耗时(ms)", max_digits=10, decimal_places=2)
    create_time = models.DateTimeField("请求时间", auto_now_add=True)

    class Meta:
        db_table = "request_log"
        verbose_name = "请求耗时记录"
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=["create_time"]),
            models.Index(fields=["method", "path"]),
        ]

    def __str__(self):
        return f"{self.method} {self.path} {self.cost_ms}ms"
