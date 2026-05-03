from .models import Book, BookReview, Bookmark, Borrow

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect



def book_detail(request, id):

    Book = Book.objects.get(pk=id)

    return render(request, 'ledger/recipe_detail.html', {
        "book": Book,
    })


class BookListView(ListView):
    model = Book
    template_name = "bookclub/book_list.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.object

        user=self.request.user

        if user.is_authenticated:
            books_bookmarked = Bookmark.objects.filter(bookmark_profile=user)
            books_bookreviewed = BookReview.objects.filter(UserReviewer=user)


        return context



class BookDetailView(DetailView):
    model = Book
    template_name = "bookclub/books_detail.html"

class BookCreateView():
    model = Book

class BookUpdateView():
    model = Book

class BookSignupView():
    model = Book