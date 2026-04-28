from django.urls import path

from .views import *

urlpatterns = [
    path("books", BooksListView.as_view(), name='books_list'),
    path('book/<int:pk>/', BookDetailView.as_view(), name='books_detail'),
    path('book/add/', BookCreateView.as_view(), name='books_add'),
    path('book/<int:pk>/edit', BookUpdateView.as_view(), name='books_edit'),
    path('book/<int:pk>/signup', BookSignupView.as_view(), name='books_signup'),


]

app_name = "bookclub"
