from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView

from .forms import *
from .models import *


class EventListView(ListView):
    model = Event
    template_name = "localevents/event_list.html"
    

class EventDetailView(DetailView):
    model = Event
    template_name = "localevents/event_detail.html"


#FIX LATER: https://stackoverflow.com/questions/18246326/how-do-i-set-user-field-in-form-to-the-currently-logged-in-user
class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    exclude = ['organizer']

    def form_valid(self, form):
        form.instance.organizer = Profile.objects.get(user=self.request.user)
        return super().form_valid(form)


class EventUpdateView(LoginRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    exclude = ['organizer']
    template_name = "localevents/event_update.html"

    #event capacity toggle here


def event_signup(request, id):
    event = Event.objects.get(pk=id)

    #replace with a proper signup template
    return render(request, "localevents/event_detail.html", {
        "event": event,
        "new_registrant": new_registrant,
    })
