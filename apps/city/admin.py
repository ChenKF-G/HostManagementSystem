from django.contrib import admin

from apps.city.models import City


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "code", "remark", "create_time"]
    search_fields = ["name", "code"]
