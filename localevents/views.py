from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy

from .forms import *
from .models import *


class EventListView(ListView): 
    model = Event
    template_name = "localevents/event_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_authenticated:
            context["all_events"] = Event.objects.all()
        else:
            users_signups = EventSignup.objects.filter(user_registrant__user=self.request.user)
            context["created_events"] = Event.objects.filter(organizer__user=self.request.user)
            #FIX SOURCE: https://docs.djangoproject.com/en/6.0/ref/models/querysets/
            context["signedup_events"] = users_signups.select_related("event").all()
            context["other_events"] = Event.objects.exclude(organizer__user=self.request.user)
        return context
    

class EventDetailView(DetailView):
    model = Event
    template_name = "localevents/event_detail.html"

    def get_context_data(self, **kwargs): #change the link
        context = super().get_context_data(**kwargs)
        return context


    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        event = self.object        
        profile = request.user.profile
        current_signups = EventSignup.objects.filter(event=event).count()
        form = RegisteredUserEventSignupForm(request.POST)

        if 'registered_user_signup' in request.POST:
            if event.event_capacity > current_signups and event.organizer != profile:
                if self.request.user.is_authenticated:
                    if form.is_valid():
                        #existing user signup automatic
                        form.save(commit=False)
                        form.event = Event.objects.get(pk=self.kwargs['pk'])
                        form.save(commit=False)
                        form.user_registrant = profile
                        return self.get(request, *args, **kwargs)
                    else:
                        self.object_list = self.get_queryset(**kwargs)
                        context = self.get_context_data(**kwargs)
                        context['form'] = form
                        return self.render_to_response(context)
                    

        return redirect(self.get_success_url())

    
    def get_success_url(self):
        return reverse_lazy('localevents:event_detail', kwargs={ 'pk': self.object.pk })


#FIX LATER: https://stackoverflow.com/questions/18246326/how-do-i-set-user-field-in-form-to-the-currently-logged-in-user
class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm


    def form_valid(self, form):
        #FIX LATER: https://stackoverflow.com/questions/17872441/django-createview-gives-an-error-needs-to-have-a-value-for-field-before-t
        #Daniel Roseman
        form.save()
        form.instance.organizer = Profile.objects.get(user=self.request.user)
        return super().form_valid(form)
    
    
    def get_success_url(self):
        return reverse_lazy('localevents:event_detail', kwargs={ 'pk': self.object.pk })


class EventUpdateView(LoginRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = "localevents/event_update.html"


    def form_valid(self, form):
        #if event is full
        event = Event.objects.get(pk=self.kwargs['pk'])
        if event.event_capacity <= EventSignup.objects.filter(event=event).count():
            form.instance.status = "Full"
        return super().form_valid(form)
    
    
    def get_success_url(self):
        return reverse_lazy('localevents:event_detail', kwargs={ 'pk': self.object.pk })


def event_signup_process(request, pk):
    event = Event.objects.get(pk=pk)
    form = NewUserEventSignupForm()

    if request.method == "POST":
        form = NewUserEventSignupForm(request.POST)

        if form.is_valid():
            event_signup = form.save(commit=False)
            event_signup.event = event
            event_signup.save()
            return redirect('localevents:event_detail', pk=event.pk)
        
    else:
        form = NewUserEventSignupForm()

    return render(request, "localevents/event_signup.html", {
        "event": event,
        "form": form,
    })
