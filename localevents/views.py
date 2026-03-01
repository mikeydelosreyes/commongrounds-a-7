from django.shortcuts import render
from django.views.generic import FormView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import *


class EventListView(ListView):
    model = Event
    template_name = #TEMPLATE TBA
    

class EventDetailView(DetailView):
    model = Event
    template_name = #TEMPLATE TBA
