from django.urls import path
from .views import patient_records, add_medical_record, edit_medical_record,medical_record_detail

urlpatterns = [
    path('<int:patient_id>/records/<int:doctor_id>/', patient_records, name='patient_records'),
    path('add_medical_record/<int:patient_id>/', add_medical_record, name='add_medical_record'),
    path('edit_medical_record/<int:record_id>/', edit_medical_record, name='edit_medical_record'),
    path('medical_record/<int:record_id>/', medical_record_detail, name='medical_record_detail'),
]
