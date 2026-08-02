"""
用户序列化器（apps/users/serializers.py）
"""
from django.contrib.auth import authenticate
from rest_framework import serializers

from apps.users.models import User


class UserLoginSerializer(serializers.Serializer):
    """登录序列化器"""

    username = serializers.CharField(required=True, max_length=50)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")
        user = authenticate(username=username, password=password)
        if user is None or not user.is_active:
            raise serializers.ValidationError("用户名或密码错误")
        attrs["user"] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    """用户信息序列化器（不含密码）"""

    class Meta:
        model = User
        fields = ["id", "username", "is_active", "last_login", "create_time"]
        read_only_fields = ["id", "create_time", "last_login"]


class UserCreateSerializer(serializers.ModelSerializer):
    """用户创建序列化器"""

    password = serializers.CharField(write_only=True, required=True, min_length=8)

    class Meta:
        model = User
        fields = ["id", "username", "password", "is_active"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            is_active=validated_data.get("is_active", True),
        )
        return user
