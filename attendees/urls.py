from django.urls import path
from .views import register_attendee, success, verify_qr

urlpatterns = [
    path('register/', register_attendee, name='register'),
    path('success/', success, name='success'),
    path('verify/', verify_qr, name='verify')
]
