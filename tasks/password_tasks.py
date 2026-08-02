"""
密码轮换任务（tasks/password_tasks.py）
"""
import logging

from celery import shared_task
from services.password_service import PasswordService

logger = logging.getLogger("celery")


@shared_task
def rotate_password_task():
    """定时轮换所有主机 root 密码（每 8 小时）"""

    logger.info("开始执行密码轮换任务")
    result = PasswordService.rotate_all()
    logger.info(f"密码轮换任务完成: {result}")
    return result
