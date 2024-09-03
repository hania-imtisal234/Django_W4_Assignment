from django.urls import path
from .views import show_appointments
from .views import list_patients
urlpatterns = [
    path('<str:user_type>/<int:user_id>/appointments/', show_appointments, name='show_appointments'),
    path('patients/', list_patients, name='list_patients'),  # New URL pattern
]
