"""
公共视图基类（apps/common/views.py）

提供 ViewSet 基类，统一接口返回封装。
"""
from rest_framework import viewsets

from utils.response import Result


class BaseModelViewSet(viewsets.ModelViewSet):
    """公共 ModelViewSet 基类"""

    # 是否通过 Service 层处理业务（子类可覆写）
    service_class = None

    def perform_create(self, serializer):
        """创建时调用 Service 层，而非直接 save"""
        if self.service_class:
            instance = self.service_class.create_host(serializer.validated_data)
        else:
            instance = serializer.save()
        return instance
