from django.contrib import admin
from .models import Project, ProjectCategory, ProjectRating, ProjectReview, Favorite, Profile


class ProjectInline(admin.TabularInline):
    model = Project


class ProjectCategoryAdmin(admin.ModelAdmin):
    model = ProjectCategory
    inlines = [ProjectInline]


class ProjectAdmin(admin.ModelAdmin):
    model = Project
    search_fields = ('title',)

    list_display = ('title', 'creator', 'category', 'created_on', 'updated_on')

    list_filter = ('created_on', 'updated_on', 'category')
    fieldsets = [
        ('Details', {
            'fields': [
                ('title', 'description', 'materials',
                 'steps'), 'category', 'creator'
            ]
        }),
    ]


class ProjectRatingAdmin(admin.ModelAdmin):
    model = ProjectRating
    list_display = ('project', 'profile', 'score')
    search_fields = ('project__title', 'profile__user__username')
    list_filter = ('score',)


class ProjectReviewAdmin(admin.ModelAdmin):
    model = ProjectReview
    list_display = ('project', 'reviewer', 'comment')
    search_fields = ('project__title',)


admin.site.register(Profile)
admin.site.register(ProjectCategory, ProjectCategoryAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectRating, ProjectRatingAdmin)
admin.site.register(ProjectReview, ProjectReviewAdmin)
