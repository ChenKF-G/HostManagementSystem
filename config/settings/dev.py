"""
开发环境配置（dev.py）
DEBUG=True，使用本地数据库，开启调试与日志输出。
"""
from .base import *  # noqa: F401,F403

DEBUG = True

# 本地开发允许所有 host
ALLOWED_HOSTS = ["*"]

# 开发环境打印 SQL
LOGGING["loggers"]["django.db.backends"] = {  # noqa: F405
    "handlers": ["console"],
    "level": "DEBUG",
    "propagate": False,
}

# 跨域（如前后端分离需要）
# CORS_ALLOW_ALL_ORIGINS = True
