from django.contrib import admin

from apps.statistics.models import HostStatistics, RequestLog


@admin.register(HostStatistics)
class HostStatisticsAdmin(admin.ModelAdmin):
    list_display = ["id", "dimension", "city", "idc", "total_count", "online_count", "offline_count", "stat_date"]
    list_filter = ["dimension", "stat_date"]


@admin.register(RequestLog)
class RequestLogAdmin(admin.ModelAdmin):
    list_display = ["id", "method", "path", "status", "ip", "cost_ms", "create_time"]
    search_fields = ["path"]
    list_filter = ["method", "status"]
    date_hierarchy = "create_time"
