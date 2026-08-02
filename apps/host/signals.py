"""
主机信号（apps/host/signals.py）

- Host 删除时自动清理其密码历史记录，保证数据一致性。
"""
import logging

from django.db.models.signals import post_delete
from django.dispatch import receiver

from apps.host.models import Host, HostPasswordHistory

logger = logging.getLogger("app")


@receiver(post_delete, sender=Host)
def clean_password_history(sender, instance, **kwargs):
    """Host 删除后清理其密码历史记录"""
    deleted, _ = HostPasswordHistory.objects.filter(host=instance).delete()
    if deleted:
        logger.info(f"主机 {instance.id} 删除，清理密码历史 {deleted} 条")
