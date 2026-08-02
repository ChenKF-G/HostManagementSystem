from django.contrib import admin

from apps.common.models import OperationLog


@admin.register(OperationLog)
class OperationLogAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "action", "resource", "resource_id", "ip", "create_time"]
    list_filter = ["action", "resource"]
    search_fields = ["resource"]
    date_hierarchy = "create_time"
