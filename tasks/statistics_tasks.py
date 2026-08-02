"""
统计任务（tasks/statistics_tasks.py）
"""
import logging

from celery import shared_task

logger = logging.getLogger("celery")


@shared_task
def generate_statistics_task():
    """生成每日主机统计（每天 00:00）"""
    from services.statistics_service import StatisticsService

    logger.info("开始执行每日统计任务")
    result = StatisticsService.generate_statistics()
    logger.info(f"每日统计任务完成: {result}")
    return result
