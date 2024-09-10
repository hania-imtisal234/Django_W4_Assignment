from django.db import models
from web.users.models import User
from django.utils import timezone



class Appointment(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ]
    doctor = models.ForeignKey(User, related_name="doctor_appointment",on_delete=models.CASCADE)
    patient = models.ForeignKey(User, related_name="patient_appointment", on_delete=models.CASCADE)
    scheduled_at = models.DateTimeField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')


    class Meta:
        unique_together = ('doctor', 'scheduled_at')
        verbose_name = 'Appointment'
        verbose_name_plural = 'Appointments'
        ordering = ['scheduled_at']

        indexes = [
            models.Index(fields=['doctor']),
            models.Index(fields=['patient']),
            models.Index(fields=['scheduled_at']),
        ]


    def __str__(self):
        return f"Appointment for {self.patient.username} with Dr. {self.doctor.username} on {self.scheduled_at}"
