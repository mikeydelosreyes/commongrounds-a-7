from django.urls import *
from .views import *

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
]

app_name = "accounts"