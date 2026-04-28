from django.db import models
from datetime import datetime
from django.urls import reverse
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User


class Genre(models.Model):

    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ['name']
        verbose_name = 'genre'
        verbose_name_plural = 'genres'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("books_list")

class Book(models.Model):
    title = models.CharField(max_length=255)
    genre = models.ForeignKey(Genre,
                              on_delete=models.SET_NULL,
                              related_name="genres")
    author = models.CharField()
    sypnopsis = models.TextField()
    publication_year = models.IntegerField()
    borrow_availability = models.BooleanField()
    created_on = models.DateTimeField(null=False,
                                      auto_now_add=True)

    updated_on = models.DateTimeField(null=False, auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("book_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ['-publication_year']
        verbose_name = 'book'
        verbose_name_plural = 'books'

class BookReview(models.Model):
    UserReviewer = models.ForeignKey(Profile,
                                     on_delete=models.CASCADE,
                                     null=True,
                                     blank=True)
    AnonReviewer = models.TextField()
    bookreview_book = models.ForeignKey(Book, 
                             verbose_name="books",
                             on_delete=models.CASCADE)
    bookreview_title = models.CharField()
    bookreview_comment = models.TextField()

class Bookmark(models.Model):
    bookmark_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    bookmark_book = models.ForeignKey(Book, on_delte=models.CASCADE)
    bookmark_date = models.DateTimeField(null=False,
                                         auto_now_add=True)




