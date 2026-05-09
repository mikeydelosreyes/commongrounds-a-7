from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import redirect_to_login
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import CreateView
from django.views.generic import UpdateView

from accounts.models import Profile
from accounts.mixins import RoleRequiredMixin
from accounts.decorators import role_required

from .models import *


class ProductListView(ListView):
    model = Product
    template_name = "merchstore/item_list.html"
    context_object_name = "products"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            try:
                user_profile = Profile.objects.get(user=self.request.user)

                # products from this prof
                user_products = Product.objects.filter(owner=user_profile)

                # all other products
                all_products = Product.objects.exclude(owner=user_profile)

                context["user_products"] = user_products
                context["all_products"] = all_products
            except Profile.DoesNotExist:
                # no prof
                context["all_products"] = Product.objects.all()
        else:
            # not logged in
            context["all_products"] = Product.objects.all()      

        # link to create 
        context["create_product_url"] = reverse_lazy("product_create")

        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "merchstore/item_detail.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()

        # user != owner
        if self.request.user.is_authenticated and product.owner != self.request.user:
            context["form"] = Transaction()
        else:
            context["form"] = None

        # user == owner
        if self.request.user.is_authenticated and product.owner == self.request.user:
            context["edit_url"] = reverse_lazy("product_update", kwargs={"pk": product.pk})

        return context

    def post(self, request, *args, **kwargs):
        product = self.get_object()

        # they can't buy their own product
        if product.owner == request.user:
            return redirect("product_detail", pk=product.pk)

        # redirect for non logged-in
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path())

        form = Transaction(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.product = product
            transaction.buyer = request.user

            # update stock 
            if product.stock > 0:
                product.stock -= transaction.quantity
                product.save()
                transaction.save()
                return redirect("cart_view")  # for CartView
            else:
                # if no stock
                return redirect("product_detail", pk=product.pk)

        # for invalid forms
        context = self.get_context_data()
        context["form"] = form
        return self.render_to_response(context)

class ProductCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    role_name = "Market Seller"
    model = Product
    template_name = "merchstore/item_form.html"
    context_object_name = "product_creator"

    fields = ["name", "product_type", "product_image", "price", "stock", "status"]

    def form_valid(self, form):
        # Set owner automatically to logged-in user's Profile
        form.instance.owner = Profile.objects.get(user=self.request.user)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass the logged-in user's Profile to the template for display
        try:
            context["owner_profile"] = Profile.objects.get(user=self.request.user)
        except Profile.DoesNotExist:
            context["owner_profile"] = None
        return context

class ProductUpdateView(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    role_name = "Market Seller"
    model = Product
    template_name = "merchstore/item_form.html"
    fields = ["name", "product_type", "description", "price", "stock", "status"]

    success_url = reverse_lazy("product_list")

    def form_valid(self, form):
        product = form.save(commit=False)

        if product.stock == 0:
            product.status = "out_of_stock"
        else:
            product.status = "available"

        product.save()
        return super().form_valid(form)

class CartView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = "merchstore/cart.html"
    context_object_name = "cart"

    def get_queryset(self):
        try:
            # converter
            user_profile = Profile.objects.get(user=self.request.user)
            return Transaction.objects.filter(Buyer=user_profile)
        except Profile.DoesNotExist:
            # empty query
            return Transaction.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        transactions = self.get_queryset()

        # group transactions
        grouped_transactions = {}
        for tx in transactions:
            owner = tx.product.owner
            if owner not in grouped_transactions:
                grouped_transactions[owner] = []
            grouped_transactions[owner].append(tx)

        context["grouped_transactions"] = grouped_transactions
        return context
    
class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = "merchstore/transactions.html"
    context_object_name = "transactions"

    def get_queryset(self):
        try:
            user_profile = Profile.objects.get(user=self.request.user)
            return Transaction.objects.filter(Product_Bought__owner=user_profile)
        except Profile.DoesNotExist:
            return Transaction.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        transactions = self.get_queryset()

        grouped_transactions = {}
        for tx in transactions:
            buyer = tx.buyer
            if buyer not in grouped_transactions:
                grouped_transactions[buyer] = []
            grouped_transactions[buyer].append(tx)

        context["grouped_transactions"] = grouped_transactions
        return context
