from django.urls import path
from .views import patient_records, add_medical_record, edit_medical_record, medical_record_detail

urlpatterns = [
    path('patients/<int:patient_id>/records/<int:doctor_id>/<int:scheduled_at>/', patient_records, name='patient_records'),
    path('patients/<int:patient_id>/records/<int:scheduled_at>/add/', add_medical_record, name='add_medical_record'),
    path('<int:record_id>/edit/', edit_medical_record, name='edit_medical_record'),
    path('detail/<int:record_id>/', medical_record_detail, name='medical_record_detail'),
]
