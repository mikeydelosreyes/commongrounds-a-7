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

class JobAdmin(admin.ModelAdmin):
    model = Job
    list_display = ('role', 'commission', 'manpower_required', 'status')
    list_filter = ('status',)   


class JobApplicationAdmin(admin.ModelAdmin):
    model = JobApplication
    list_display = ('applicant', 'job', 'status', 'applied_on')
    list_filter = ('status',)

admin.site.register(CommissionType)
admin.site.register(Commission)
admin.site.register(Job)
admin.site.register(JobApplication)