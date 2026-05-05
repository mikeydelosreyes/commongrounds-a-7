from django.urls import path

from .views import permission_denied, ProfileUpdateView, seller_dashboard

app_name = "accounts"

urlpatterns = [
    path("<str:username>/", ProfileUpdateView.as_view(), name="profile_update"),
]