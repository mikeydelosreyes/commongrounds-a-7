
from django import forms
from .models import *


class BookReviewForm(forms.ModelForm):
    class Meta:
        model = BookReview
        fields = ["bookreview_title", "bookreview_comment"]

class BookBorrowForm(forms.ModelForm):
    class Meta:
        model = Borrow
        fields = ["bookreview_title", "bookreview_comment"]

class BookContributeForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["bookreview_title", "bookreview_comment"]

class BookFormFactory(forms.ModelForm):
    class Meta:
        model = BookReview
        fields = ["bookreview_title", "bookreview_comment"]