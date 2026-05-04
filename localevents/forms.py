from django import forms

from .models import *

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'category', 'event_image', 'description', 'location',
                'organizer', 'start_time', 'end_time', 'event_capacity', 'status',]
        widgets = {
            'start_time': forms.TextInput(
                attrs={ 'type': 'datetime-local' }
            ),
            'end_time': forms.TextInput(
                attrs={ 'type': 'datetime-local' }
            )
        }

class EventSignupForm(forms.ModelForm):
    class Meta:
        model = EventSignup
        fields = ['event', 'new_registrant',]