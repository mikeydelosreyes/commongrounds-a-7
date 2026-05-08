from .models import Book, BookReview, Bookmark, Borrow
from .forms import *

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import render, redirect

from accounts.models import Profile


def book_detail(request, id):

    Book = Book.objects.get(pk=id)

    return render(request, 'bookclub/book_detail.html', {
        "book": Book,
    })





class BookListView(ListView):
    model = Book
    template_name = "bookclub/book_list.html"
    context_object_name = "all_books"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        

        

        if self.request.user.is_authenticated:
            profile, created = Profile.objects.get_or_create(user=self.request.user)

            books_contributed = Book.objects.all()




            books_bookmarked = Book.objects.filter(
                bookmarked_book__bookmark_profile=profile
            ).distinct()

            books_reviewed = Book.objects.filter(
                reviewed_books__UserReviewer=profile
            ).distinct()

            grouped_books = (
                books_bookmarked | books_reviewed
            ).distinct()
            
            all_books = Book.objects.exclude(
                id__in=grouped_books.values_list("id", flat=True)
            )

            context["contributed_books"] = books_contributed
            context["bookmarked_book"] = books_bookmarked
            context["reviewed_books"] = books_reviewed
            context["all_books"] = all_books


        return context
    



"""
There should be a button that allows you to bookmark the book. The number of bookmarks on the book should also be displayed.
There should be a Form that is rendered on this view that allows you to review the book. When the user is logged in, the review is automatically assigned to the Profile with the associated display name. Else, the display name should be “Anonymous”.
There should be a button to borrow a book that will lead to the borrow view.
In this view, if the Book’s contributor is the logged-in user, there should be an edit link that will lead to the update view.
The list of book reviews should be shown.

"""

class BookDetailView(DetailView):
    model = Book

    template_name = "bookclub/book_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user=self.request.user
        book = self.get_object()
        context["is_authenticated"] = user.is_authenticated

        if not user.is_authenticated:
            context["is_bookmarked"] = False
            context["review"] = BookReview.objects.all().last().bookreview_comment
        else:
            profile  = Profile.objects.get(user=user)
            review=BookReview.objects.filter(bookreview_book=book, 
                                  UserReviewer=profile).exists()
            context["reviewer"] = self.request.user.profile.name
        
            if review and user.is_authenticated:
                context["review"] = BookReview.objects.get(
                                            bookreview_book=book, 
                                            UserReviewer=profile).bookreview_comment
                context["is_bookmarked"] = book.bookmarked_book.filter(
                    bookmark_profile=user.profile
                ).exists() 
            context["bookmark_count"] = book.bookmarked_book.count()
            context["reviews"] = book.bookmarked_book.count()
        

        return context
    def post(self, request, *args, **kwargs):
        user=self.request.user
        book = self.get_object()
        action = request.POST.get('action')

        if user.is_authenticated:
            profile, created = Profile.objects.get_or_create(user=self.request.user)
            bookmark = Bookmark.objects.filter(bookmark_profile=profile, bookmark_book=book)
            bookreview = BookReview.objects.filter(UserReviewer=profile, bookreview_book=book)



        if action=='toggle_bookmark':
            if not request.user.is_authenticated:
                return redirect('login')
            
            if  bookmark.exists():
                bookmark.delete()
            else:
                bookmark.create(bookmark_profile=profile, bookmark_book=book)

        if action=='submit_review':
            content = request.POST.get('review_content')

            if not request.user.is_authenticated and content:
                BookReview.objects.create( 
                    bookreview_book=book, 
                    bookreview_comment=content
                )
            elif content:
                BookReview.objects.create(
                    UserReviewer=profile, 
                    bookreview_book=book, 
                    bookreview_comment=content
                )
        
        
            
        
        return redirect('bookclub:book_detail', pk=book.pk)




class BookCreateView(LoginRequiredMixin, CreateView):
    role_required="Book Contributer"
    model = Book
    form_class = BookContributeForm
    template_name = "bookclub/book_create.html"

    def form_valid(self, form):
        book = form.save(commit=False)

        book.save()
        self.object = book

        return super().form_valid(form)


class BookUpdateView(LoginRequiredMixin, UpdateView):
    role_required="Book Contributer"
    model = Book
    form_class = BookContributeForm
    template_name = "bookclub/book_update.html"

    def form_valid(self, form):
        book = form.save(commit=False)

        book.save()
        self.object = book

        return super().form_valid(form)
    


class BookBorrowView(CreateView):
    model = Borrow
    form_class = BookBorrowForm
    template_name = "bookclub/book_borrow.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["book"] = Book.objects.get()

    def get_initial(self):
        initial = super().get_initial()

        if self.request.user.is_authenticated:
            initial["borrower_name"] = str(
                self.request.user.profile
            )



