from django.contrib import admin
from .models import *


class EventInLine(admin.TabularInline):
    model = Event


class EventTypeAdmin(admin.ModelAdmin):
    model = EventType
    inlines = [EventInLine,]


class EventSignupInLine(admin.TabularInline):
    model = EventSignup


class EventAdmin(admin.ModelAdmin):
    model = Event

    search_fields = ('title', )

    list_display = ('title', 'location', 'start_time', 'end_time',)

    list_filter = ('title', 'location',)  

    fieldsets = [
        ('Details', {
            'fields': [
                ('title', 'location', 'start_time', 'end_time', 'event_capacity',),
                'organizer',
                'category',
                'event_image',
                'description',
                'status',
            ]
        }),
    ]

    inlines = [EventSignupInLine,]


admin.site.register(EventType, EventTypeAdmin)
admin.site.register(Event, EventAdmin)