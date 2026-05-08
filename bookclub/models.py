from django.db import models
from django.urls import reverse

import sys

from accounts.models import Profile


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
        return reverse("book_list")


class Book(models.Model):
    title = models.CharField(max_length=255)
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        related_name="books",
        null=True)
    contributor = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="contributed_books")
    author = models.CharField()
    sypnopsis = models.TextField()
    publication_year = models.IntegerField()
    borrow_availability = models.BooleanField()
    created_on = models.DateTimeField(null=True,
                                      auto_now_add=True)

    updated_on = models.DateTimeField(null=True, auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('bookclub:book_detail', args=[str(self.pk)])

    class Meta:
        ordering = ['-publication_year']
        verbose_name = 'book'
        verbose_name_plural = 'books'

class BookReview(models.Model):
    UserReviewer = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="reviewer"
    )
    AnonReviewer = models.TextField(default="Text")
    bookreview_book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="reviewed_books"
    )
    bookreview_title = models.CharField(max_length=255)
    bookreview_comment = models.TextField()

    class Meta:
        verbose_name = 'review'
        verbose_name_plural = 'reviews'

class Bookmark(models.Model):
    bookmark_profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="bookmarker",
        null=True, blank=True
    )
    bookmark_book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="bookmarked_book",
        null=True, blank=True
    )
    bookmark_date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'bookmark'
        verbose_name_plural = 'bookmarks'

    

class Borrow(models.Model):
    borrow_book = models.ForeignKey(
        Book, 
        on_delete=models.CASCADE,
        related_name="borrowed_book"    
    )
    borrower = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="borrower"
    )
    book_name = models.CharField(max_length=255, blank=True, null=True)
    book_borrowdate = models.DateField()
    borrow_returndate = models.DateField()

    def get_absolute_url(self):
        return reverse('bookclub:book_borrow', args=[str(self.borrow_book.pk)])
    
    class Meta:
        verbose_name = 'borrowed'
        verbose_name_plural = 'multiple_borrowed'

