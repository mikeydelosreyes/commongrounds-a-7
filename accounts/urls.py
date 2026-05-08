from django.urls import *
from .views import *

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('<str:username>/', ProfileUpdateView.as_view(), name="profile_update"),
]


app_name = "accounts"