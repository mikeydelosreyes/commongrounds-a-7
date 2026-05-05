from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView

from .decorators import role_required
from .forms import ProfileForm
from .models import Profile


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = "accounts/displayname_update.html"

    def get_object(self, queryset=None):
        return get_object_or_404(Profile, user__username=self.kwargs["username"])

    def get_success_url(self):
        return reverse_lazy(
            "accounts:profile_update", kwargs={"username": self.kwargs["username"]}
        )

