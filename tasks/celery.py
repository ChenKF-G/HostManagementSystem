"""
Celery 应用实例（tasks/celery.py）
"""
import logging
import os

from celery import Celery

# 设置 Django 配置模块
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")

app = Celery("host_manager")

# 从 Django settings 加载 Celery 配置
app.config_from_object("django.conf:settings", namespace="CELERY")

# 初始化 Django（加载 INSTALLED_APPS、LOGGING 等配置）
import django  # noqa: E402

django.setup()

# 让 Celery 使用 Django 的 LOGGING 配置，而非自己接管根日志
app.conf.update(
    worker_hijack_root_logger=False,
    # 将 stdout/stderr 重定向到 Celery 日志（写文件可实时刷新）
    worker_redirect_stdouts_level="INFO",
)

# 自动发现任务
app.autodiscover_tasks()
