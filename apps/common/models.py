"""
公共模型（apps/common/models.py）
"""
from django.conf import settings
from django.db import models


class TimeStampedModel(models.Model):
    """抽象基类：提供 create_time / update_time 通用字段"""

    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now=True)

    class Meta:
        abstract = True


class OperationLog(models.Model):
    """
    操作日志模型
    对应数据表 operation_log：记录用户关键写操作。
    """
    ACTION_CHOICES = [
        ("create", "新增"),
        ("update", "更新"),
        ("delete", "删除"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="操作用户",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column="user",
    )
    action = models.CharField("操作类型", max_length=50, choices=ACTION_CHOICES)
    resource = models.CharField("操作资源", max_length=50)
    resource_id = models.BigIntegerField("资源 ID", null=True, blank=True)
    detail = models.JSONField("操作详情", null=True, blank=True)
    ip = models.CharField("请求 IP", max_length=45, null=True, blank=True)
    create_time = models.DateTimeField("操作时间", auto_now_add=True)

    class Meta:
        db_table = "operation_log"
        verbose_name = "操作日志"
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=["resource", "resource_id"]),
        ]

    def __str__(self):
        return f"{self.resource}:{self.action}"
