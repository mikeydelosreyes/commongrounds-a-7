from django.urls import path

from .views import *

urlpatterns = [
    path("books", RecipeListView.as_view(), name='recipeslist'),
    path('book/<int:pk>/', RecipeDetailView.as_view(), name='recipe'),

]

app_name = "bookclub"
