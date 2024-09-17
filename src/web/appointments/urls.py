from django.urls import path

from .views import AppointmentListView, PatientListView, ReportingView


urlpatterns = [
    path('<str:user_type>/<int:user_id>/detail/',
         AppointmentListView.as_view(), name='show_appointments'),
    path('patients/', PatientListView.as_view(),
         name='list_patients'),
    path('<str:user_type>/list/', ReportingView.as_view(), name='reporting_view')
]
