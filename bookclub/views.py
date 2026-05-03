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
    context_object_name = "all_books"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user=self.request.user

        if user.is_authenticated:
            
            books_contributed = Book.objects


            books_bookmarked = Book.objects.filter(
                bookmarked_books__bookmark_profile=user
            ).distinct()

            books_reviewed = Book.objects.filter(
                reviewed_books__UserReviewer=user
            ).distinct()

            grouped_books = (
                books_bookmarked | books_reviewed
            ).distinct()
            
            all_books = Book.objects.exclude(
                id__in=grouped_books.values_list("id", flat=True)
            )

            context["contributed_books"] = books_contributed
            context["bookmarked_books"] = books_bookmarked
            context["reviewed_books"] = books_reviewed
            context["all_books"] = all_books


        return context


"""
There should be a display whether the book is available to be borrowed.
There should be a button that allows you to bookmark the book. The number of bookmarks on the book should also be displayed.
There should be a Form that is rendered on this view that allows you to review the book. When the user is logged in, the review is automatically assigned to the Profile with the associated display name. Else, the display name should be “Anonymous”.
There should be a button to borrow a book that will lead to the borrow view.
In this view, if the Book’s contributor is the logged-in user, there should be an edit link that will lead to the update view.
The list of book reviews should be shown.

"""

class BookDetailView(DetailView):
    model = Book
    template_name = "bookclub/books_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user=self.request.user

        if user.is_authenticated:
            
            books_contributed = Book.objects


            books_bookmarked = Book.objects.filter(
                bookmarked_books__bookmark_profile=user
            ).distinct()

            books_reviewed = Book.objects.filter(
                reviewed_books__UserReviewer=user
            ).distinct()

            grouped_books = (
                books_bookmarked | books_reviewed
            ).distinct()
            
            all_books = Book.objects.exclude(
                id__in=grouped_books.values_list("id", flat=True)
            )

            context["contributed_books"] = books_contributed
            context["bookmarked_books"] = books_bookmarked
            context["reviewed_books"] = books_reviewed
            context["all_books"] = all_books


        return context


class BookCreateView():
    model = Book

class BookUpdateView():
    model = Book

class BookBorrowView():
    model = Book