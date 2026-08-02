"""
根路由（config/urls.py）
注册所有业务应用路由、认证路由、Swagger 文档路由。
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from config.views import test_page

urlpatterns = [
    # 管理后台
    path("admin/", admin.site.urls),
    # API 根
    path("api/", include("config.api_urls")),
    # Swagger 文档
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    # 前端测试台页面（静态文件托管）
    path("test/", test_page, name="test-page"),
]

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
