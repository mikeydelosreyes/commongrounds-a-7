from datetime import datetime
from django.db import models
from django.core.validators import *
from django.urls import *
from accounts.models import Profile

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
                                  related_name='event_types', null=True)
    organizer = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    event_image = models.ImageField(upload_to='images/', null=False)
    description = models.TextField()
    location = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    event_capacity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    #fix source: https://docs.djangoproject.com/en/6.0/ref/models/fields/
    AVAILABLE = "Available"
    FULL = "Full"
    DONE = "Done"
    CANCELLED = "Cancelled"
    STATUS_CHOICES = {
        AVAILABLE: "Available",
        FULL: "Full",
        DONE: "Done",
        CANCELLED: "Cancelled",
    }
    status = models.CharField(
        max_length=63,
        choices=STATUS_CHOICES,
        default=AVAILABLE,
    )
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


class EventSignup(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE,
                                  related_name='events', null=True)
    user_registrant = models.ForeignKey(Profile, on_delete=models.SET_NULL,
                                  related_name='user_registrants', null=True, blank=True)
    new_registrant = models.CharField(max_length=255, null=True, blank=True)