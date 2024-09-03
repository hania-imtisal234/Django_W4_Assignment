from django.urls import path
from .views import show_appointments

urlpatterns = [
    path('<str:user_type>/<int:user_id>/appointments/', show_appointments, name='show_appointments'),
]
