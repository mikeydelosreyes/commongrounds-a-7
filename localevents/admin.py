from django.contrib import admin
from .models import *


class EventInLine(admin.TabularInline):
    model = Event


class EventTypeAdmin(admin.ModelAdmin):
    model = EventType
    inlines = [EventInLine,]


class EventAdmin(admin.ModelAdmin):
    model = Event

    search_fields = ('title', )

    list_display = ('title', 'location', 'start_time', 'end_time',)

    list_filter = ('location', 'start_time', 'end_time',)  

    fieldsets = [
        ('Details', {
            'fields': [
                ('title', 'location', 'start_time', 'end_time'), 'category',
            ]
        }),
    ]

admin.site.register(EventType, EventTypeAdmin)
admin.site.register(Event, EventAdmin)