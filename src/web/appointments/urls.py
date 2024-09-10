from django.urls import path
from .views import show_appointments
from .views import list_patients
from .views import reporting_view


urlpatterns = [
    path('<str:user_type>/<int:user_id>/detail/', show_appointments, name='show_appointments'),
    path('patients/', list_patients, name='list_patients'),  # New URL pattern
    path('<str:user_type>/list/',reporting_view, name='reporting_view'),
]
