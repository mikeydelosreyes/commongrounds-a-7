from django import forms

from django.forms import inlineformset_factory

from .models import *

class CommissionForm(forms.ModelForm):
    class Meta:
        model = Commission
        fields = ['title', 'description', 'type', 'people_required', 'status']
        exclude = ['maker']


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['role', 'manpower_required', 'status']

JobFormSet = inlineformset_factory(Commission, 
                                   Job, 
                                   fields=['role', 'manpower_required', 'status',],
                                   extra=2,
                                   can_delete=True)

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = []