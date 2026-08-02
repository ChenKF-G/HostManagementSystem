"""
城市模型（apps/city/models.py）

对应数据表 city：
- name 唯一，非空
- code 唯一（如 BJ），非空
"""
from django.db import models

from apps.common.models import TimeStampedModel


class City(TimeStampedModel):
    name = models.CharField("城市名称", max_length=50, unique=True)
    code = models.CharField("城市编码", max_length=20, unique=True)
    remark = models.CharField("备注", max_length=255, null=True, blank=True)

    class Meta:
        db_table = "city"
        verbose_name = "城市"
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["code"]),
        ]

    def __str__(self):
        return self.name
