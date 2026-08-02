"""
权限类（utils/permissions.py）

基于 Django 的 is_active 等属性进行细粒度权限控制。
"""
from rest_framework.permissions import BasePermission


class IsActiveUser(BasePermission):
    """仅允许启用的用户访问"""

    message = "用户未启用，无法访问"

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_active)


class IsSuperUser(BasePermission):
    """仅允许超级管理员访问（可扩展）"""

    message = "需要管理员权限"

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_superuser)
