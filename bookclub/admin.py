from django.contrib import admin
from .models import Genre, Book


class BookInLine(admin.TabularInline):
    model = Book


class GenreAdmin(admin.ModelAdmin):
    model = Genre
    inlines = [BookInLine,]


class BookAdmin(admin.ModelAdmin):
    model = Book

    search_fields = ('title', )

    list_display = ('title', 'publication_year')

    list_filter = ('publication_year',)

    fieldsets = [

        ('Details', {
            'fields': [
                ('title', 'author', 'publication_year' ), 'genre'
            ]
        }),
    ]


admin.site.register(Genre, GenreAdmin)
admin.site.register(Book, BookAdmin)
