from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from web.users.models import User
from web.appointments.models import Appointment
from django.utils import timezone
from datetime import datetime


class PermissionAndObjectMixin:
    """
    Mixin to handle common permission checks and object fetching.
    """

    def get_appointment(self):
        patient = get_object_or_404(User, id=self.kwargs['patient_id'])
        doctor = get_object_or_404(User, id=self.kwargs['doctor_id'])
        scheduled_datetime = timezone.make_aware(
            datetime.fromtimestamp(
                int(self.kwargs['scheduled_at'])), timezone.get_current_timezone()
        )

        if not self.has_permission(patient, doctor):
            raise PermissionDenied(
                "You do not have permission to view or modify this data.")

        return get_object_or_404(
            Appointment.objects.select_related('patient', 'doctor'),
            patient=patient, doctor=doctor, scheduled_at=scheduled_datetime
        )

    def has_permission(self, patient, doctor):
        """
        Check if the current user has permission to view or edit the appointment.
        """
        return (self.request.user == patient or
                self.request.user == doctor or
                self.request.user.is_staff or
                self.request.user.is_superuser)

    def get_patient_and_doctor(self):
        appointment = self.get_appointment()
        return appointment.patient, appointment.doctor
