"""
公共配置（base.py）
所有环境共享的基础配置：应用注册、中间件、数据库、日志等。
敏感信息（SECRET_KEY、数据库、密钥）从环境变量读取，通过 .env 注入。
"""
import os
import sys
from datetime import timedelta
from pathlib import Path

from celery.schedules import crontab
from dotenv import load_dotenv

# ============================================================
# 基础路径配置
# ============================================================
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# 加载 .env 环境变量（在根目录）
load_dotenv(BASE_DIR / ".env")

# 将项目根目录、config、apps 加入 sys.path，保证各模块可被 import
sys.path.insert(0, str(BASE_DIR))
sys.path.insert(0, str(BASE_DIR / "config"))
sys.path.insert(0, str(BASE_DIR / "apps"))

# ============================================================
# 安全配置
# ============================================================
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
DEBUG = False
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "*").split(",")

# ============================================================
# 应用注册
# ============================================================
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 第三方
    "rest_framework",
    "django_filters",
    "django_celery_beat",
    "drf_spectacular",
    # 业务应用
    "apps.users",
    "apps.city",
    "apps.idc",
    "apps.host",
    "apps.statistics",
    "apps.common",
]

# ============================================================
# 中间件
# ============================================================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # 自定义请求耗时统计中间件
    "middleware.request_time.RequestTimeMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# ============================================================
# 数据库（MySQL）
# ============================================================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.environ.get("DB_NAME", "host_manager"),
        "USER": os.environ.get("DB_USER", "root"),
        "PASSWORD": os.environ.get("DB_PASSWORD", "123456"),
        "HOST": os.environ.get("DB_HOST", "127.0.0.1"),
        "PORT": os.environ.get("DB_PORT", "3306"),
        "OPTIONS": {
            "charset": "utf8mb4",
            # 关闭 STRICT 模式，保证兼容
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# ============================================================
# 密码哈希（Django 内置 PBKDF2）
# ============================================================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# 自定义用户模型（app_label 为 users）
AUTH_USER_MODEL = "users.User"

# ============================================================
# 国际化
# ============================================================
LANGUAGE_CODE = "zh-hans"
TIME_ZONE = "Asia/Shanghai"
USE_I18N = True
USE_TZ = True

# ============================================================
# 静态文件与媒体
# ============================================================
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

# ============================================================
# Django REST Framework 配置
# ============================================================
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PAGINATION_CLASS": "utils.pagination.StandardPagination",
    "PAGE_SIZE": 10,
    "EXCEPTION_HANDLER": "utils.exceptions.custom_exception_handler",
    "DEFAULT_RENDERER_CLASSES": [
        "utils.response.CustomJSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
}

# ============================================================
# Simple JWT 配置
# ============================================================
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=2),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "ALGORITHM": "HS256",
    "SIGNING_KEY": os.environ.get("JWT_SECRET_KEY", SECRET_KEY),
}

# ============================================================
# drf-spectacular Swagger 配置
# ============================================================
SPECTACULAR_SETTINGS = {
    "TITLE": "Host Manager API",
    "DESCRIPTION": "主机管理系统 API 文档",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "COMPONENT_SPLIT_REQUEST": True,
}

# ============================================================
# Celery 配置（Redis 作为 Broker / Backend）
# ============================================================
REDIS_URL = os.environ.get("REDIS_URL", "redis://127.0.0.1:6379/0")
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_TIME_LIMIT = 30 * 60  # 单个任务最长执行时间
CELERY_BEAT_SCHEDULE = {
    "rotate-password-every-8-hours": {
        "task": "tasks.password_tasks.rotate_password_task",
        "schedule": crontab(hour="*/8", minute=0),
    },
    "generate-statistics-daily": {
        "task": "tasks.statistics_tasks.generate_statistics_task",
        "schedule": crontab(hour=0, minute=0),
    },
    # 临时测试调度：每 30 秒执行一次统计任务（验证 beat 自动投递，测试后可删除）
    "test-every-30-seconds": {
        "task": "tasks.statistics_tasks.generate_statistics_task",
        "schedule": timedelta(seconds=30),
    },
}

# ============================================================
# 加密密钥（Fernet）
# ============================================================
ENCRYPT_KEY = os.environ.get("ENCRYPT_KEY", "m2e08--CH4UP_gwXLZNZY4XVRvM3a8vP8JmL_wTqQyY=")

# ============================================================
# 日志配置（LOGGING）
# ============================================================
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "app_file": {
            "level": "INFO",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": str(LOG_DIR / "app.log"),
            "when": "midnight",
            "backupCount": 7,
            "formatter": "verbose",
            "encoding": "utf-8",
        },
        "error_file": {
            "level": "ERROR",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": str(LOG_DIR / "error.log"),
            "when": "midnight",
            "backupCount": 30,
            "formatter": "verbose",
            "encoding": "utf-8",
        },
        "celery_file": {
            "level": "INFO",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": str(LOG_DIR / "celery.log"),
            "when": "midnight",
            "backupCount": 14,
            "formatter": "verbose",
            "encoding": "utf-8",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "app_file"],
            "level": "INFO",
            "propagate": False,
        },
        "django.request": {
            "handlers": ["error_file"],
            "level": "ERROR",
            "propagate": False,
        },
        "celery": {
            "handlers": ["console", "celery_file"],
            "level": "INFO",
            "propagate": False,
        },
        "app": {
            "handlers": ["console", "app_file"],
            "level": "INFO",
            "propagate": False,
        },
        "error": {
            "handlers": ["console", "error_file"],
            "level": "ERROR",
            "propagate": False,
        },
    },
}

# 默认主键类型
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
