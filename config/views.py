"""
根级视图（config/views.py）
"""
from django.conf import settings
from django.http import HttpResponse


def test_page(request):
    """返回前端测试台静态页面"""
    file_path = settings.BASE_DIR / "static" / "test" / "index.html"
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    return HttpResponse(content, content_type="text/html; charset=utf-8")
