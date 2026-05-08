
from django import forms
from .models import *


class BookReviewForm(forms.ModelForm):
    class Meta:
        model = BookReview
        fields = '__all__'

class BookBorrowForm(forms.ModelForm):

    class Meta:
        model = Borrow
        fields = ['borrower_name', 'book_borrowdate']
class BookContributeForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        

