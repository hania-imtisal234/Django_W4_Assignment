from web.users.models import User
from .models import Appointment
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.core.cache import cache
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from .models import Appointment
from web.users.models import User


class PatientListView(ListView):
    model = Appointment
    template_name = 'appointments/list_patients.html'
    context_object_name = 'appointments'
    cache_timeout = 60 * 15

    def get_queryset(self):
        user = self.request.user
        cache_key = f"patient_appointments_{user.id}"
        queryset = cache.get(cache_key)

        if queryset is None:
            if not (user.groups.filter(name='doctor').exists() or user.is_superuser):
                raise PermissionDenied(
                    "You do not have permission to view this page.")

            if user.groups.filter(name='doctor').exists():
                queryset = Appointment.objects.filter(doctor=user).distinct()
            else:
                queryset = Appointment.objects.all()

            cache.set(cache_key, queryset, timeout=self.cache_timeout)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AppointmentListView(ListView):
    model = Appointment
    template_name = 'appointments/appointments.html'
    context_object_name = 'appointments'
    ordering = '-scheduled_at'
    cache_timeout = 60 * 15  # Cache timeout in seconds (15 minutes)

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        user_type = self.kwargs.get('user_type')
        user = get_object_or_404(User, id=user_id)

        is_doctor = self.request.user.groups.filter(name='doctor').exists()
        is_patient = self.request.user.groups.filter(name='patient').exists()
        is_superuser = self.request.user.is_superuser

        # Generate a unique cache key based on user and filters
        cache_key = f"appointments_{user_id}_{
            user_type}_{self.request.user.id}"
        queryset = cache.get(cache_key)

        if queryset is None:
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

            # Cache the queryset
            cache.set(cache_key, queryset, timeout=self.cache_timeout)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_type'] = self.kwargs.get('user_type')
        context['user_id'] = self.kwargs.get('user_id')
        return context
