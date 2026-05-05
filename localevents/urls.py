from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import *

urlpatterns = [
    path('events', EventListView.as_view(), name='event_list'),
    path('event/<int:pk>', EventDetailView.as_view(), name='event_detail'),
    path('event/add', EventCreateView.as_view(), name='event_create'),
    path('event/<int:pk>/edit', EventUpdateView.as_view(), name='event_update'),
    path('event/<int:pk>/signup', event_signup_process, name='event_signup'),
    ]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


app_name = "localevents"