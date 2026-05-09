from django.urls import path, include

from .views import ProfileUpdateView

app_name = "accounts"

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('<str:username>/', ProfileUpdateView.as_view(), name="profile_update"),
]


app_name = "accounts"
