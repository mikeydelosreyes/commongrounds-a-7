from django.shortcuts import redirect
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

from .strategies import OwnProductsStrategy, OtherProductsStrategy, AllProductsStrategy

from .models import *


class ProductListView(ListView):

    model = Product
    template_name = "merchstore/item_list.html"
    context_object_name = "products"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            try:
                context["user_products"] = OwnProductsStrategy().filter(self.request.user)
                context["all_products"] = OtherProductsStrategy().filter(self.request.user)
            except Profile.DoesNotExist:
                context["all_products"] = AllProductsStrategy().filter(self.request.user)
        else:
            context["all_products"] = AllProductsStrategy().filter(self.request.user)

        context["create_product_url"] = reverse_lazy("product_create")
        return context


class ProductDetailView(DetailView):

    model = Product
    template_name = "merchstore/item_detail.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()

        if self.request.user.is_authenticated:
            try:
                user_profile = Profile.objects.get(user=self.request.user)

                # if logged-in user is not the owner
                if product.owner != user_profile:
                    context["form"] = Transaction()
                else:
                    context["form"] = None
                    context["edit_url"] = reverse_lazy(
                        "product_update", kwargs={"pk": product.pk}
                    )
            except Profile.DoesNotExist:
                # no Profile exists for this user
                context["form"] = None
        else:
            context["form"] = None

        return context

    def post(self, request, *args, **kwargs):
        product = self.get_object()

        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path())

        form = Transaction(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.Product_Bought = product
            transaction.Buyer = Profile.objects.get(user=request.user)
            transaction.save()  # Observer (signal) will handle stock update
            return redirect("cart_view")

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
