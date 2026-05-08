from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic.edit import UpdateView
from .models import Profile
from .forms import ProfileForm
from django.template.defaultfilters import slugify


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = "accounts/displayname_update.html"

    slug_field = "user__username"
    slug_url_kwarg = "username"

    def get_object(self, queryset=None):
        return Profile.objects.get(
            user__username=self.kwargs["username"]
        )