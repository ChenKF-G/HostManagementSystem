from django.contrib import admin

from apps.idc.models import IDC


@admin.register(IDC)
class IDCAdmin(admin.ModelAdmin):
    list_display = ["id", "city", "name", "code", "address", "create_time"]
    search_fields = ["name", "code"]
    list_filter = ["city"]
