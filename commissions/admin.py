from django.contrib import admin
from .models import *


class CommissionTypeAdmin(admin.ModelAdmin):
    model = CommissionType


class CommissionAdmin(admin.ModelAdmin):
    model = Commission

    search_fields = ('title', )

    list_display = ('title', 'people_required',
                    "created_on", "status", "maker")

    list_filter = ('title', 'people_required')

    fieldsets = [
        ('Details', {
            'fields': [
                ('title', 'people_required', 'status', 'maker')
            ]
        })
    ]


class JobAdmin(admin.ModelAdmin):
    model = Job
    list_display = ('role', 'commission', 'manpower_required', 'status')
    list_filter = ('status',)


class JobApplicationAdmin(admin.ModelAdmin):
    model = JobApplication
    list_display = ('applicant', 'job', 'status', 'applied_on')
    list_filter = ('status',)


admin.site.register(CommissionType, CommissionTypeAdmin)
admin.site.register(Commission, CommissionAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(JobApplication, JobApplicationAdmin)
