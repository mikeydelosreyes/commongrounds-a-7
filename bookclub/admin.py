from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Profile
from .models import Genre, Book


class GenreAdmin(admin.ModelAdmin):
    model = Genre


class BookAdmin(admin.ModelAdmin):
    model = Book

    search_fields = ('name', )

    list_display = ('name', 'due_date')

    list_filter = ('due_date',)

    fieldsets = [

        ('Details', {
            'fields': [
                ('name', 'due_date'), 'Genre'
            ]
        }),
    ]


admin.site.register(Genre, GenreAdmin)
admin.site.register(Book, BookAdmin)
