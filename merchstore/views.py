from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import redirect_to_login
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import CreateView
from django.views.generic import UpdateView

from .models import *


class ProductListView(ListView):
    model = Product
    template_name = "merchstore/item_list.html"
    context_object_name = "products"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            # posted products
            user_products = Product.objects.filter(owner=self.request.user)

            # other products
            all_products = Product.objects.exclude(owner=self.request.user)

            context["user_products"] = user_products
            context["all_products"] = all_products
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

class ProductCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Product
    template_name = "merchstore/item_form.html"
    context_object_name = "product_creator"

    def form_valid(self, form):
        # auto owner to logged-in
        form.instance.owner = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
       return hasattr(self.request.user, 
                      "profile") and self.request.user.profile.role == "Market Seller"

class ProductUpdateView(UpdateView):
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

    def test_func(self):
        # market seller code
        return hasattr(self.request.user, "profile") and self.request.user.profile.role == "Market Seller"

class CartView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = "merchstore/cart.html"
    context_object_name = "transactions"

    def get_queryset(self):
        # buyer = user
        return Transaction.objects.filter(buyer=self.request.user)

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
    template_name = "merchstore/transaction_list.html"
    context_object_name = "transactions"

    def get_queryset(self):
        return Transaction.objects.filter(product__owner=self.request.user)

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
