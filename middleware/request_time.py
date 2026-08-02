"""
请求耗时统计中间件（middleware/request_time.py）

职责：统计每个 HTTP 请求的处理耗时，并记录请求上下文。

记录字段：
- URL / Method / Status / IP / 耗时(ms) / 用户

处理逻辑：
1. 请求进入时记录开始时间；
2. 获取请求上下文（method、path、IP、用户）；
3. 执行后续处理（get_response）；
4. 请求返回后计算耗时；
5. 写入日志 + 落库到 request_log 表。
"""
import logging
import time

logger = logging.getLogger("app")


def get_client_ip(request) -> str:
    """获取客户端真实 IP（兼容反向代理 X-Forwarded-For）"""
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    if xff:
        return xff.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "")


class RequestTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.perf_counter()

        # 跳过静态文件与文档请求，减少噪音（可选）
        response = self.get_response(request)

        cost = round((time.perf_counter() - start) * 1000, 2)
        user = getattr(request, "user", None)
        client_ip = get_client_ip(request)

        # 写日志
        logger.info(
            f"{request.method} {request.path} {response.status_code} "
            f"{cost:.2f}ms IP={client_ip} user={user if user and user.is_authenticated else '-'}"
        )

        # 落库到 request_log，供前端/报表查询
        try:
            from apps.statistics.models import RequestLog

            RequestLog.objects.create(
                user=user if user and user.is_authenticated else None,
                method=request.method,
                path=request.path[:255],
                status=response.status_code,
                ip=client_ip[:45],
                cost_ms=cost,
            )
        except Exception as e:  # noqa: BLE001
            # 落库失败不影响请求主流程，仅记录日志
            logger.warning(f"request_log 落库失败: {e}")

        return response
