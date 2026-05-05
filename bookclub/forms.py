
from django import forms
from .models import *


class BookReviewForm(forms.ModelForm):
    class Meta:
        model = BookReview
        fields = ["bookreview_title", "bookreview_comment"]

class BookBorrowForm(forms.ModelForm):
    class Meta:
        model = Borrow
        fields = ["book_name", "book_borrowdate", "borrow_returndate"]

class BookContributeForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "genre", "author"]
