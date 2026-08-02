"""
统一返回格式封装（utils/response.py）

所有接口返回统一结构：
{
    "code": 200,
    "message": "success",
    "data": {}
}
"""
from rest_framework.renderers import JSONRenderer


class Result:
    """统一返回工具类"""

    @staticmethod
    def success(data=None, message="success", code=200):
        return {"code": code, "message": message, "data": data}

    @staticmethod
    def fail(message="操作失败", code=400, data=None):
        return {"code": code, "message": message, "data": data}


class CustomJSONRenderer(JSONRenderer):
    """
    自定义 JSON 渲染器：
    拦截 DRF 的正常响应，统一包装为 {code, message, data} 结构。
    """

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context.get("response") if renderer_context else None
        status_code = response.status_code if response else 200

        # 已包装过（例如异常处理器返回的）则直接透传
        if isinstance(data, dict) and "code" in data and "message" in data:
            return super().render(data, accepted_media_type, renderer_context)

        # 非 2xx 状态码，统一按失败处理
        if not (200 <= status_code < 300):
            message = data.get("detail") if isinstance(data, dict) else str(data)
            result = Result.fail(message=message or "请求失败", code=status_code)
        else:
            result = Result.success(data=data)

        renderer_context["response"].status_code = status_code
        return super().render(result, accepted_media_type, renderer_context)
