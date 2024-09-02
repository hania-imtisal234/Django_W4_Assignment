from django.db import models
from web.users.models import Doctor
from web.patient.models import Patient
from django.utils import timezone



class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    scheduled_at = models.DateTimeField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Appointment for {self.patient.name} with Dr. {self.doctor.user.first_name} {self.doctor.user.last_name} on {self.scheduled_at}"



