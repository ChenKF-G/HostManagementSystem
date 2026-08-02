"""
统一分页（utils/pagination.py）

列表接口统一支持 page / page_size 参数，返回统一分页结构。
"""
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from utils.response import Result


class StandardPagination(PageNumberPagination):
    """标准分页类"""

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data):
        """将分页结果包装为统一返回结构"""
        return Response(
            Result.success(
                data={
                    "items": data,
                    "pagination": {
                        "page": self.page.number,
                        "page_size": self.get_page_size(self.request),
                        "total": self.page.paginator.count,
                        "pages": self.page.paginator.num_pages,
                    },
                }
            )
        )
