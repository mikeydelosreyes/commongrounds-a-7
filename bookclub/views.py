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



class BookDetailView(DetailView):
    model = Book
    template_name = "bookclub/books_detail.html"

class BookCreateView():
    model = Book

class BookUpdateView():
    model = Book

class BookSignupView():
    model = Book