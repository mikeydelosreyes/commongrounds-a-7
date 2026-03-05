from .models import Book
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

class BookListView(ListView):
    model = Book
    template_name = "bookclub/book_list.html"


class BookDetailView(DetailView):
    model = Book
    template_name = "bookclub/book_detail.html"
