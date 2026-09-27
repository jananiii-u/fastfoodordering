from django.contrib import admin
from .models import Table


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = (
        'table_number',
        'qr_token',
        'is_active',
    )

    list_filter = (
        'is_active',
    )

    search_fields = (
        'table_number',
        'qr_token',
    )