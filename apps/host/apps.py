from django.apps import AppConfig


class HostConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.host"
    verbose_name = "主机管理"

    def ready(self):
        """注册信号处理器"""
        import apps.host.signals  # noqa: F401
