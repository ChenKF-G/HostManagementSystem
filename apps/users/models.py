"""
用户模型（apps/users/models.py）

对应数据表 sys_user，继承 Django AbstractUser 以复用密码哈希（PBKDF2）。
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """自定义用户模型"""

    # AbstractUser 已包含 username / password / is_active / last_login 等
    is_active = models.BooleanField(verbose_name="是否启用", default=True)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now=True)

    class Meta:
        db_table = "sys_user"
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
