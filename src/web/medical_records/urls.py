from django.urls import path
from .views import AddMedicalRecordView, EditMedicalRecordView, MedicalRecordDetailView, PatientRecordDetailView

urlpatterns = [
    path('patients/<int:patient_id>/records/<int:doctor_id>/<int:scheduled_at>/',
         PatientRecordDetailView.as_view(), name='patient_records'),
    path('patients/<int:patient_id>/records/<int:scheduled_at>/add/',
         AddMedicalRecordView.as_view(), name='add_medical_record'),
    path('<int:pk>/edit/', EditMedicalRecordView.as_view(),
         name='edit_medical_record'),
    path('detail/<int:pk>/', MedicalRecordDetailView.as_view(),
         name='medical_record_detail'),
]
