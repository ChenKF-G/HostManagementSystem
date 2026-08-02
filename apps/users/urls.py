"""
用户认证路由（apps/users/urls.py）
"""
from django.urls import path

from apps.users.views import LoginView, MeView, RefreshView

urlpatterns = [
    path("login", LoginView.as_view(), name="auth-login"),
    path("refresh", RefreshView.as_view(), name="auth-refresh"),
    path("me", MeView.as_view(), name="auth-me"),
]
