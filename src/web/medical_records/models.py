# web/medical_records/models.py

from django.db import models
from web.patient.models import Patient
from web.users.models import Doctor

class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment = models.ForeignKey('appointments.Appointment', null=True, blank=True, on_delete=models.SET_NULL)
    diagnosis = models.TextField()
    treatment = models.TextField()
    notes = models.TextField()
    report = models.FileField(upload_to='medical_records/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set the timestamp
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'Record for {self.patient.name}'
