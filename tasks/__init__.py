"""
Celery 应用与任务包（tasks）

创建 Celery 应用实例，并注册密码轮换 / 统计两个定时任务。

说明：autodiscover_tasks() 默认只扫描各 Django app 内的 tasks.py，
而本项目任务位于根级 tasks/ 包中，故需在此显式导入以保证任务注册。
"""
from .celery import app as celery_app

# 显式导入任务模块，确保任务被 Celery 注册
from . import password_tasks  # noqa: F401,E402
from . import statistics_tasks  # noqa: F401,E402

__all__ = ("celery_app",)
