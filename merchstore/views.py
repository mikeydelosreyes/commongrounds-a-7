from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import *

class MerchListView(ListView):
    model = Product
    template_name = "merchstore/item_list.html"

class MerchDetailView(DetailView):
    model = Product
    template_name = "merchstore/item_detail.html"
