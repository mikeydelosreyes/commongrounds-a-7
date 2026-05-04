from django import forms

from django.forms import inlineformset_factory

from .models import *

class CommissionForm(forms.ModelForm):
    class Meta:
        model = Commission
        fields = ["title", "description",
                  "type", "status",
                  "people_required",]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'maker' in self.fields:
            self.fields['maker'].disabled = True


JobFormSet = inlineformset_factory(
    Commission,
    Job,
    fields=['role', 'manpower_required', 'status'], 
    extra=1,
    can_delete=True
)

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = []