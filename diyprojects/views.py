from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import (LoginRequiredMixin, 
                                        UserPassesTestMixin)
from django.db.models import Q, Avg
from django.shortcuts import render, redirect
from .models import *
from .forms import *


class ProjectListView(ListView):
    model = Project
    template_name = 'diyprojects/project_list.html'

    def get_queryset(self):
        queryset = Project.objects.all()
        if self.request.user.is_authenticated:
            profile = self.request.user.profile
            queryset = queryset.filter(
                Q(creator=profile) |
                Q(favorites__profile=profile) |
                Q(reviews__reviewer=profile)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = Project.objects.all().distinct()
        return context



class ProjectDetailView(DetailView):
    model = Project
    template_name = 'diyprojects/project_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()
        context['favorites'] = project.favorites.count()
        average_score = project.ratings.aggregate(Avg('score'))['score__avg']
        context['average_score'] = average_score
        context['rating_form'] = ProjectRatingForm()
        context['review_form'] = ProjectReviewForm()
        context['reviews'] = project.reviews.all()
        return context
    
    def post(self, request, *arg, **kwaargs):
        project =  self.get_object()
        profile = request.user.profile

        if 'check_favortie' in request.POST:
            favorite = Favorite.objects.filter(project = project, profile = profile).exists()
            
            if favorite:
                Favorite.objects.filter(project=project, profile=profile).delete()
            else:
                Favorite.objects.create(project=project, profile=profile)

        
          
       

class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm

    def form_invalid(self, form):
        form.instance.profile = Profile.objects.get(user=self.request.user)
        return super().form_invalid(form)
    