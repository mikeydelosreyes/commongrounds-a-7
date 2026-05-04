from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from .models import *
from .forms import *


class ProjectListView(ListView):
    model = Project
    template_name = 'diyprojects/project_list.html'


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'diyprojects/project_detail.html'

class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm

    def form_invalid(self, form):
        form.instance.profile = Profile.objects.get(user=self.request.user)
        return super().form_invalid(form)
    