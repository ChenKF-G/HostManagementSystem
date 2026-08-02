"""
API 子路由（config/api_urls.py）
汇总所有业务应用的 API 路由。
"""
from django.urls import include, path

urlpatterns = [
    # 认证
    path("auth/", include("apps.users.urls")),
    # 城市
    path("", include("apps.city.urls")),
    # 机房
    path("", include("apps.idc.urls")),
    # 主机
    path("", include("apps.host.urls")),
    # 统计
    path("", include("apps.statistics.urls")),
    # 请求耗时记录
    path("", include("apps.statistics.request_log_urls")),
]
