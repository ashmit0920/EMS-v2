from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_attendee, name='register'),
    path('success/<str:attendee_id>', views.success, name='success'),
    path('verify/', views.verify_qr, name='verify'),
    path('qr_code/<str:attendee_id>/', views.view_qr, name='get_qr_code')
]
