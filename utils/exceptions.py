"""
全局异常处理（utils/exceptions.py）

将各类异常统一转换为规范返回格式，避免堆栈信息泄露给客户端。

覆盖异常类型：
- ValidationError    -> 400 参数错误
- NotFound           -> 404 资源不存在
- PermissionDenied   -> 403 无权限
- AuthenticationFailed -> 401 认证失败
- 未捕获异常         -> 500 服务器内部错误
"""
import logging

from django.db import IntegrityError
from rest_framework.views import exception_handler

from constants.response_code import (
    HTTP_BAD_REQUEST,
    HTTP_FORBIDDEN,
    HTTP_INTERNAL_ERROR,
    HTTP_NOT_FOUND,
    HTTP_UNAUTHORIZED,
    PARAM_ERROR,
    SERVER_ERROR,
)
from utils.response import Result

logger = logging.getLogger("error")


def custom_exception_handler(exc, context):
    """
    自定义 DRF 异常处理器：
    返回结构统一为 {code, message, data}。
    """
    # 优先调用 DRF 内置处理器，拿到标准响应
    response = exception_handler(exc, context)

    if response is not None:
        # 依据 HTTP 状态码映射业务 code 与 message
        status = response.status_code
        if status == HTTP_BAD_REQUEST:
            code, message = PARAM_ERROR, "参数错误"
            # 提取具体校验错误信息
            detail = response.data
            if isinstance(detail, dict) and detail:
                message = _extract_error_message(detail)
            elif isinstance(detail, list) and detail:
                message = str(detail[0])
        elif status == HTTP_UNAUTHORIZED:
            code, message = HTTP_UNAUTHORIZED, "认证失败或 Token 无效"
        elif status == HTTP_FORBIDDEN:
            code, message = HTTP_FORBIDDEN, "无权限"
        elif status == HTTP_NOT_FOUND:
            code, message = HTTP_NOT_FOUND, "资源不存在"
        else:
            code, message = status, str(response.data)
        response.data = Result.fail(message=message, code=code)
        return response

    # 唯一约束冲突
    if isinstance(exc, IntegrityError):
        logger.error("数据库唯一约束冲突: %s", exc)
        return _fail_response("数据冲突（唯一约束违反）", HTTP_BAD_REQUEST, PARAM_ERROR)

    # 未捕获异常
    logger.exception("未捕获异常: %s", exc)
    return _fail_response("服务器内部错误", HTTP_INTERNAL_ERROR, SERVER_ERROR)


def _fail_response(message, status, code, data=None):
    """构造标准失败响应"""
    from django.http import JsonResponse

    return JsonResponse(Result.fail(message=message, code=code, data=data), status=status)


def _extract_error_message(detail: dict) -> str:
    """从校验错误 dict 中提取第一条可读错误信息"""
    for key, value in detail.items():
        if isinstance(value, list) and value:
            return f"{key}: {value[0]}"
        return f"{key}: {value}"
    return "参数错误"
