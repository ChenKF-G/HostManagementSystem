"""
JWT 生成/校验工具（utils/jwt.py）

基于 rest_framework_simplejwt 实现 access/refresh token 生成与自定义认证。
"""
import jwt
from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken


def generate_tokens(user) -> dict:
    """为用户生成 access / refresh token"""
    refresh = RefreshToken.for_user(user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }


def decode_token(token: str) -> dict:
    """校验并解码 JWT（可选，用于自定义校验）"""
    return jwt.decode(
        token,
        settings.SIMPLE_JWT.get("SIGNING_KEY", settings.SECRET_KEY),
        algorithms=[settings.SIMPLE_JWT.get("ALGORITHM", "HS256")],
    )


class CustomJWTAuthentication(JWTAuthentication):
    """
    自定义 JWT 认证类：
    继承 simplejwt 的 JWTAuthentication，从请求头 Authorization: Bearer <token> 解析。
    用于统一认证入口，便于后续扩展（如黑名单校验）。
    """
