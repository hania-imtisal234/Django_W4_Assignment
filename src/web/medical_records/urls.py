from django.urls import path
from .views import patient_records, add_medical_record, edit_medical_record

urlpatterns = [
    path('<str:user_type>/<int:patient_id>/records/<int:doctor_id>/', patient_records, name='patient_records'),
    path('<str:user_type>/add_medical_record/<int:patient_id>/', add_medical_record, name='add_medical_record'),
    path('<str:user_type>/edit_medical_record/<int:record_id>/', edit_medical_record, name='edit_medical_record'),
]
