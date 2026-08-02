"""
操作日志服务（services/operation_log_service.py）

负责记录用户关键写操作（create/update/delete），落库到 operation_log 表。
"""
import logging

from apps.common.models import OperationLog

logger = logging.getLogger("app")


class OperationLogService:
    @staticmethod
    def record(request, action: str, resource: str, resource_id=None, detail=None) -> None:
        """
        记录操作日志。
        :param request: 请求对象（用于取用户与 IP）
        :param action: create / update / delete
        :param resource: host / city / idc 等
        :param resource_id: 资源 ID
        :param detail: 操作详情
        """
        user = getattr(request, "user", None)
        user_id = user.id if user and user.is_authenticated else None

        ip = request.META.get("HTTP_X_FORWARDED_FOR", "").split(",")[0].strip() or request.META.get("REMOTE_ADDR", "")

        OperationLog.objects.create(
            user_id=user_id,
            action=action,
            resource=resource,
            resource_id=resource_id,
            detail=detail,
            ip=ip[:45],
        )
        logger.info(f"操作日志: {user} {action} {resource}:{resource_id}")
