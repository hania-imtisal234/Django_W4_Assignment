from .views import show_appointments
from django.urls import path, include

urlpatterns = [
    path('', show_appointments, name='show_appointments'),
]