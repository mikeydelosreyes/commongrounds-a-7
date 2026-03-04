from django.urls import path

from .views import *

urlpatterns = [
    path("books", BooksListView.as_view(), name='recipeslist'),
    path('book/<int:pk>/', BookDetailView.as_view(), name='recipe'),

]

app_name = "bookclub"
