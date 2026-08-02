"""
生产环境配置（prod.py）
DEBUG=False，使用远程数据库，安全加固。
"""
from .base import *  # noqa: F401,F403

DEBUG = False

# 生产环境必须显式指定允许的主机，禁止使用 *
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")  # noqa: F405

# 安全头配置（HTTPS 相关）
SECURE_SSL_REDIRECT = os.environ.get("SECURE_SSL_REDIRECT", "False") == "True"
SESSION_COOKIE_SECURE = os.environ.get("SESSION_COOKIE_SECURE", "False") == "True"
CSRF_COOKIE_SECURE = os.environ.get("CSRF_COOKIE_SECURE", "False") == "True"
SECURE_HSTS_SECONDS = int(os.environ.get("SECURE_HSTS_SECONDS", "0"))
