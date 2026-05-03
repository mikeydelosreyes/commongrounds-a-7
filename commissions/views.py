from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView

from .models import *


class CommissionListView(ListView):
    model = Commission
    template_name = "commissions/commissions_list.html"


class CommissionDetailView(DetailView):
    model = Commission
    template_name = "commissions/commissions_detail.html"


class CommissionCreateView(CreateView):
    model = Commission
    template_name = "commissions/commissions_create.html"  


class CommissionUpdateView(UpdateView):
    model = Commission
    template_name = "commissions/commissions_update.html"    
