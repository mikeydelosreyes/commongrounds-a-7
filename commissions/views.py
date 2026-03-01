from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

class CommissionListView(ListView):
    model = Commission
    template_name = "commissions/commissions_list.html"

class CommissionDetailView(DetailView):
    model = Commission
    template_name = "commissions/commissions_detail.html"
