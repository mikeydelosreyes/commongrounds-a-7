from django.urls import path

from .views import *

urlpatterns = [
    path("books", BookListView.as_view(), name='books_list'),
    path('book/<int:pk>/', BookDetailView.as_view(), name='books_detail'),
    path("book/add", BookCreateView.as_view(), name='books_create'),
    path("book/<int:pk>/edit", BookUpdateView.as_view(), name='books_update'),
    path("book/<int:pk>/borrow", BookBorrowView.as_view(), name='books_borrow'), 
]

app_name = "bookclub"
