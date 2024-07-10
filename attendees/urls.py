from django.urls import path
from .views import register_attendee, success

urlpatterns = [
    path('register/', register_attendee, name='register'),
    path('success/', success, name='success'),
]
