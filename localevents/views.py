from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy

from .forms import *
from .models import *


class EventListView(ListView): #fix the order
    model = Event
    template_name = "localevents/event_list.html"
    

class EventDetailView(DetailView): #fix the button
    model = Event
    template_name = "localevents/event_detail.html"


#FIX LATER: https://stackoverflow.com/questions/18246326/how-do-i-set-user-field-in-form-to-the-currently-logged-in-user
class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm


    def form_valid(self, form):
        #FIX LATER: https://stackoverflow.com/questions/17872441/django-createview-gives-an-error-needs-to-have-a-value-for-field-before-t
        #Daniel Roseman
        form.save()
        form.instance.organizer.add(Profile.objects.get(user=self.request.user))
        return super().form_valid(form)
    
    
    def get_success_url(self):
        return reverse_lazy('localevents:event_detail', kwargs={ 'pk': self.object.pk })


class EventUpdateView(LoginRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = "localevents/event_update.html"

    #event capacity toggle here


def event_signup_process(request, pk):
    event = Event.objects.get(pk=pk)
    form = EventSignupForm()

    if request.method == "POST":
        form = EventSignupForm(request.POST)

        if form.is_valid():
            event_signup = form.save(commit=False)
            event_signup.event = event
            event_signup.save()
            return redirect('localevents:event_detail', pk=event.pk)
        
    else:
        form = EventSignupForm()

    return render(request, "localevents/event_signup.html", {
        "event": event,
        "form": form,
    })
