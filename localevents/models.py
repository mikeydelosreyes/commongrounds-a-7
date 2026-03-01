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
