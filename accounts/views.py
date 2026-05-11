from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic.edit import UpdateView, CreateView
from .models import Profile
from .forms import ProfileForm
<<<<<<< HEAD
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
=======
from django.urls import reverse_lazy

>>>>>>> diyprojects

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = "accounts/displayname_create.html"

    def get_object(self, queryset=None):
        profile, _ = Profile.objects.get_or_create(
        user=self.request.user,
        defaults={"name": self.request.user.username, "email": self.request.user.email},
    )
        return profile

    def get_success_url(self):
        return reverse_lazy(
            "accounts:profile_update", kwargs={"username": self.kwargs["username"]}
        )
