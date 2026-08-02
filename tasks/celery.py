"""
Celery 应用实例（tasks/celery.py）
"""
import os

from celery import Celery

# 设置 Django 配置模块
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")

app = Celery("host_manager")

# 从 Django settings 加载 Celery 配置
app.config_from_object("django.conf:settings", namespace="CELERY")

# 自动发现任务
app.autodiscover_tasks()
