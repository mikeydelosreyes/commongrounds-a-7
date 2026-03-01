from django.contrib import admin
from .models import *

class CommissionInline(admin.TabularInline):
    model = Commission


class CommissionTypeAdmin(admin.modelAdmin):
    model = CommissionType
    inlines = [CommissionInline, ]


class CommissionAdmin(admin.modelAdmin):
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

admin.site.register(CommissionType, CommissionTypeAdmin)
admin.site.register(Commission, CommissionAdmin)
