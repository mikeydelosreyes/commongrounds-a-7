from datetime import datetime
from django.db import models
from django.urls import *

class EventType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('eventtype_list', args=[str(self.name)])
    

    class Meta:
        ordering = ['name']
        verbose_name = 'event type'
        verbose_name_plural = 'event types'


class Event(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(EventType, on_delete=models.SET_NULL,
                                  related_name='events', null=True)
    description = models.TextField()
    location = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('localevents:event_detail', args=[str(self.pk)])
    

    class Meta:
        ordering = ['-created_on']
        verbose_name = 'event'
        verbose_name_plural = 'events'