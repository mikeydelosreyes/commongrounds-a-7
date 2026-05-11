from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy

from .forms import *
from .models import *
from accounts.mixins import *


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
            context["other_events"] = Event.objects.exclude(organizer__user=self.request.user).exclude(id__in=users_signups.select_related("event").all())
                                                    
        return context
    

class EventDetailView(DetailView):
    model = Event
    template_name = "localevents/event_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        event = self.get_object()
        organizer = event.organizer

        if user.is_authenticated and user.profile == organizer:
            context["is_organizer"] = True

        else:
            context["is_organizer"] = False

        context["is_authenticated"] = user.is_authenticated
        context["form"] = RegisteredUserEventSignupForm()
        context["current_signups"] = EventSignup.objects.filter(event=event).count()
        return context


    def post(self, request, *args, **kwargs):
        user = self.request.user
        event = self.get_object()
        action = request.POST.get("action")

        if user.is_authenticated:
            profile = self.request.user.profile

        if action == "sign_up":
            if user.is_authenticated:
                EventSignup.objects.create(event=event, user_registrant = profile)

        return redirect('localevents:event_detail', pk=event.pk)

    
    def get_success_url(self):
        return reverse_lazy('localevents:event_detail', kwargs={ 'pk': self.kwargs['pk']})


#FIX LATER: https://stackoverflow.com/questions/18246326/how-do-i-set-user-field-in-form-to-the-currently-logged-in-user
class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    role_name = "Event Organizer"

    def get_context_data(self, **kwargs): #change the link
        context = super().get_context_data(**kwargs)
        return context


    def form_valid(self, form):
        #FIX LATER: https://stackoverflow.com/questions/17872441/django-createview-gives-an-error-needs-to-have-a-value-for-field-before-t
        #Daniel Roseman
        form.save()
        form.instance.organizer = Profile.objects.get(user=self.request.user)
        return super().form_valid(form)
    
    
    def get_success_url(self):
        return reverse_lazy('localevents:event_detail', kwargs={ 'pk': self.object.pk })


class EventUpdateView(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = "localevents/event_update.html"
    role_name = "Event Organizer"


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
