"""
用户认证视图（apps/users/views.py）

提供登录、刷新 Token、当前用户信息接口。
"""
from django.utils import timezone
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import permissions, serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.serializers import UserLoginSerializer, UserSerializer
from utils.jwt import generate_tokens
from utils.response import Result


class TokenSerializer(serializers.Serializer):
    """登录成功返回的 Token 信息"""

    access = serializers.CharField()
    refresh = serializers.CharField()
    user = UserSerializer()


class RefreshRequestSerializer(serializers.Serializer):
    """刷新 Token 请求体"""

    refresh = serializers.CharField()


class AccessTokenSerializer(serializers.Serializer):
    """刷新 Token 返回体"""

    access = serializers.CharField()


@extend_schema_view(
    post=extend_schema(
        summary="登录",
        request=UserLoginSerializer,
        responses={200: TokenSerializer},
    )
)
class LoginView(APIView):
    """登录：POST /api/auth/login"""

    permission_classes = [permissions.AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        # 记录最后登录时间
        user.last_login = timezone.now()
        user.save(update_fields=["last_login"])

        tokens = generate_tokens(user)
        return Response(
            Result.success(
                data={
                    **tokens,
                    "user": UserSerializer(user).data,
                }
            ),
            status=status.HTTP_200_OK,
        )


@extend_schema_view(
    post=extend_schema(
        summary="刷新 Token",
        request=RefreshRequestSerializer,
        responses={200: AccessTokenSerializer},
    )
)
class RefreshView(APIView):
    """刷新 Token：POST /api/auth/refresh"""

    permission_classes = [permissions.AllowAny]
    serializer_class = RefreshRequestSerializer

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response(Result.fail(message="缺少 refresh token", code=400))
        try:
            refresh = RefreshToken(refresh_token)
            return Response(
                Result.success(data={"access": str(refresh.access_token)})
            )
        except Exception:  # noqa: BLE001
            return Response(Result.fail(message="refresh token 无效", code=401))


@extend_schema_view(
    get=extend_schema(
        summary="当前用户信息",
        responses={200: UserSerializer},
    )
)
class MeView(APIView):
    """当前用户信息：GET /api/auth/me"""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request):
        return Response(
            Result.success(data=UserSerializer(request.user).data),
            status=status.HTTP_200_OK,
        )
