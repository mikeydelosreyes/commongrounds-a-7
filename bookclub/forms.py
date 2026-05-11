
from django import forms
from .models import *


class BookCreateForm(forms.ModelForm):

    class Meta:
        model = Book
        exclude = ['contributor']
        widgets = {'genre': forms.Select()}


class BookUpdateForm(forms.ModelForm):
    class Meta:
        model = Book
        exclude = ['contributor']
        widgets = {'genre': forms.Select()}


class BookBorrowForm(forms.ModelForm):

    class Meta:
        model = Borrow
        fields = ['book_name', 'book_borrowdate']
