from django.apps import AppConfig


class StatisticsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.statistics"
    verbose_name = "主机统计与请求日志"
