from django.db import models
from django.contrib.auth.models import *
from django.urls import *
from django.template.defaultfilters import slugify

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=63)
    email = models.EmailField(max_length=254)
    role = models.CharField(max_length=63, null=True, blank=True)

    def __str__(self):
        return self.user.username

    @property
    def slug(self):
        return slugify(self.user.username)
