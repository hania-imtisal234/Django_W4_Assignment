from django.db import models
from web.users.models import User
from django.utils import timezone



class Appointment(models.Model):
    doctor = models.ForeignKey(User, related_name="doctor_appointment",on_delete=models.CASCADE)
    patient = models.ForeignKey(User, related_name="patient_appointment", on_delete=models.CASCADE)
    scheduled_at = models.DateTimeField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Appointment for {self.patient.name} with Dr. {self.doctor.name} on {self.scheduled_at}"



