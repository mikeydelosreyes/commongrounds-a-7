from django.db import models
from  datetime import datetime
from django.urls import reverse
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

class Genre(models.Model):

    name=models.CharField(max_length=255)
    description=models.TextField()
    