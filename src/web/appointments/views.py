from django.views.generic import ListView
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from .models import Appointment
from web.users.models import User


class AppointmentListView(ListView):
    model = Appointment
    template_name = 'appointments/appointments.html'
    context_object_name = 'appointments'
    ordering = '-scheduled_at'

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        user_type = self.kwargs.get('user_type')
        user = get_object_or_404(User, id=user_id)

        is_doctor = self.request.user.groups.filter(name='doctor').exists()
        is_patient = self.request.user.groups.filter(name='patient').exists()
        is_superuser = self.request.user.is_superuser

        queryset = Appointment.objects.select_related(
            'doctor', 'patient').order_by(self.ordering)

        if is_superuser:
            if user_type == 'doctor':
                queryset = queryset.filter(doctor=user_id)
            elif user_type == 'patient':
                queryset = queryset.filter(patient=user_id)
            else:
                raise PermissionDenied(
                    "You do not have permission to view these appointments.")
        elif is_doctor:
            if user_type == 'doctor' and self.request.user == user:
                queryset = queryset.filter(doctor=self.request.user)
            else:
                raise PermissionDenied(
                    "You do not have permission to view other doctors' appointments.")
        elif is_patient:
            if user_type == 'patient' and self.request.user == user:
                queryset = queryset.filter(patient=self.request.user)
            else:
                raise PermissionDenied(
                    "You do not have permission to view other patients' appointments.")
        else:
            raise PermissionDenied(
                "You do not have permission to view these appointments.")

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_type'] = self.kwargs.get('user_type')
        context['user_id'] = self.kwargs.get('user_id')
        return context


class PatientListView(ListView):
    model = Appointment
    template_name = 'appointments/list_patients.html'
    context_object_name = 'appointments'
    distinct = True

    def get_queryset(self):
        user = self.request.user
        if not (user.groups.filter(name='doctor').exists() or user.is_superuser):
            raise PermissionDenied(
                "You do not have permission to view this page.")
        if user.groups.filter(name='doctor').exists():
            return Appointment.objects.filter(doctor=user).distinct()
        else:
            return Appointment.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
