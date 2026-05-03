from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView

from .models import *


class EventListView(ListView):
    model = Event
    template_name = "localevents/event_list.html"
    

class EventDetailView(DetailView):
    model = Event
    template_name = "localevents/event_detail.html"

class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm


    def form_valid(self, form):
        form.instance.profile = Profile.objects.get(user=self.request.user)
        return super().form_valid(form)

class EventUpdateView(LoginRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = "localevents/event_update.html"