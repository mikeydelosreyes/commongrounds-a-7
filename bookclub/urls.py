from django.urls import path

from .views import *

urlpatterns = [
    path("books", BooksListView.as_view(), name='books_list'),
    path('book/<int:pk>/', BookDetailView.as_view(), name='books_detail'),

]

app_name = "bookclub"
