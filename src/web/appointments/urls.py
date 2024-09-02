from django.urls import path
from .views import show_appointments

urlpatterns = [
    path('appointments/', show_appointments, name='show_appointments'),
]
