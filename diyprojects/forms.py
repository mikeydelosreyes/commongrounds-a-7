from django import forms
from .models import *

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'category', 'description', 'materials','steps']

class ProjectFavoriteForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_status']

class ProjectReviewForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['comment', 'image']

class ProjectRatingForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['score']

