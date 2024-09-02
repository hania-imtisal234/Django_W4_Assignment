from django.db import models
from web.users.models import Doctor
from web.patient.models import Patient
from web.appointments.models import Appointment
from django.utils import timezone



class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    diagnosis = models.TextField()
    treatment = models.TextField()
    notes = models.TextField(blank=True, null=True)
    report = models.FileField(upload_to='reports/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Medical Record for {self.patient.name} from {self.doctor.user.first_name} {self.doctor.user.last_name}"
