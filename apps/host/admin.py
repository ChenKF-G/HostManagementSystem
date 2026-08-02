from django.contrib import admin

from apps.host.models import Host, HostPasswordHistory


@admin.register(Host)
class HostAdmin(admin.ModelAdmin):
    list_display = ["id", "hostname", "ip", "port", "idc", "status", "os_type", "create_time"]
    search_fields = ["hostname", "ip"]
    list_filter = ["status", "idc"]


@admin.register(HostPasswordHistory)
class HostPasswordHistoryAdmin(admin.ModelAdmin):
    list_display = ["id", "host", "is_active", "valid_from", "expire_at", "create_time"]
    list_filter = ["is_active"]
