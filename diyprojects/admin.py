from django.contrib import admin
from .models import Project, ProjectCategory
# Register your models here.

class ProjectInline(admin.TabularInline):
    model = Project

class ProjectCategoryAdmin(admin.ModelAdmin):
    model = ProjectCategory
    inlines = [ProjectInline]

class ProjectAdmin(admin.ModelAdmin):
    model = Project

    search_fields = ('title', )

    list_display = ('title', 'created_on', 'updated_on')

    list_filter = ('created_on', 'updated_on')  

    fieldsets = [
        ('Details', {
            'fields': [
                ('title', 'created_on', 'category'),
            ]
        }),
    ]

admin.site.register(ProjectCategory, ProjectCategoryAdmin)
admin.site.register(Project, ProjectAdmin)
