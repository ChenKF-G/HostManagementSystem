"""
Celery 应用与任务包（tasks）

创建 Celery 应用实例，并自动发现任务。
"""
from .celery import app as celery_app

__all__ = ("celery_app",)
