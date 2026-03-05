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

    search_fields = ('title', )

    list_display = ('title', 'publication_year')

    list_filter = ('publication_year',)

    fieldsets = [

        ('Details', {
            'fields': [
                ('title', 'author', 'publication_year' ), 'Genre'
            ]
        }),
    ]


admin.site.register(Genre, GenreAdmin)
admin.site.register(Book, BookAdmin)
