from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .models import Book, Genre

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from django.contrib.auth.views import PasswordResetDoneView
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.views import PasswordResetCompleteView
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User


class BooksListView(ListView):
    model = Book
    template_name = "bookclub/book_list.html"


class BookDetailView(DetailView):
    model = Book
    template_name = "bookclub/book_detail.html"
