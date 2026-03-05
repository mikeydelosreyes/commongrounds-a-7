from django.contrib import admin
from .models import *


class CommissionTypeAdmin(admin.ModelAdmin):
    model = CommissionType


class CommissionAdmin(admin.ModelAdmin):
    model = Commission

    search_fields = ('title', )

    list_display = ('title', 'people_required')

    list_filter = ('title', 'people_required')

    fieldsets = [
        ('Details', {
            'fields': [
                ('title', 'people_required')
            ]
        })
    ]


admin.site.register(CommissionType)
admin.site.register(Commission)
