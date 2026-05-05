
from django import forms
from .models import *


class BookReviewForm(forms.ModelForm):
    class Meta:
        model = BookReview
        fields = '__all__'

class BookBorrowForm(forms.ModelForm):
    class Meta:
        model = Borrow
        fields = '__all__'

class BookContributeForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if self.instance and self.instance.pk:
            self.fields['role_required'].disabled = True
        else:
            self.initial['role_required'] = "Book Contributor"
