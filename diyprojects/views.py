from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import ProjectCategory, Project


class ProjectListView(ListView):
    model = Project
    template_name = 'diyprojects/project_list.html'


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'diyprojects/project_detail.html'

