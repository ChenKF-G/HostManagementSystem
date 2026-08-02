"""
Host Manager 项目配置入口
配置文件路径：config.settings.dev（开发环境）
"""
import os

# 默认使用开发环境配置
DJANGO_SETTINGS_MODULE = os.environ.get("DJANGO_SETTINGS_MODULE", "config.settings.dev")

application = None  # 在 wsgi/asgi 中赋值
