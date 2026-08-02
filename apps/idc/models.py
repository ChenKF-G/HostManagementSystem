"""
机房模型（apps/idc/models.py）

对应数据表 idc：
- city 外键关联城市
- (city, name) 联合唯一
- code 唯一
"""
from django.db import models

from apps.city.models import City
from apps.common.models import TimeStampedModel


class IDC(TimeStampedModel):
    city = models.ForeignKey(
        City, verbose_name="所属城市", on_delete=models.CASCADE, related_name="idcs"
    )
    name = models.CharField("机房名称", max_length=50)
    code = models.CharField("机房编码", max_length=20, unique=True)
    address = models.CharField("机房地址", max_length=255, null=True, blank=True)

    class Meta:
        db_table = "idc"
        verbose_name = "机房"
        verbose_name_plural = verbose_name
        constraints = [
            models.UniqueConstraint(fields=["city", "name"], name="uniq_city_idc_name")
        ]

    def __str__(self):
        return f"{self.city.name}-{self.name}"
