"""
自定义校验器（utils/validators.py）
"""
import ipaddress

from django.core.exceptions import ValidationError
from rest_framework import serializers


def validate_ip(value):
    """校验 IP 地址（IPv4/IPv6）合法性"""
    try:
        ipaddress.ip_address(value)
    except ValueError:
        raise serializers.ValidationError("IP 地址格式非法")
    return value


def validate_port(value):
    """校验 SSH 端口范围（1-65535）"""
    if not (1 <= value <= 65535):
        raise serializers.ValidationError("端口必须在 1-65535 之间")
    return value
