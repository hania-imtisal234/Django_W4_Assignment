from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from .models import Appointment
from web.users.models import User


@login_required
@permission_required('appointments.view_appointment', raise_exception=True)
def show_appointments(request, user_id, user_type):
    try:
        user = get_object_or_404(User, id=user_id)

        if request.user.is_superuser:
            if user_type == 'doctor':
                appointments = Appointment.objects.filter(
                    doctor=user_id).order_by('-scheduled_at')
            else:
                appointments = Appointment.objects.filter(
                    patient=user_id).order_by('-scheduled_at')
        elif request.user.groups.filter(name='doctor').exists() and user_type == 'doctor':
            if request.user == user:
                appointments = Appointment.objects.filter(
                    doctor=request.user).order_by('-scheduled_at')
            else:
                raise PermissionDenied(
                    "You do not have permission to view other doctors' appointments.")

        elif request.user.groups.filter(name='patient').exists() and user_type == 'patient':
            if request.user == user:
                appointments = Appointment.objects.filter(
                    patient=request.user).order_by('-scheduled_at')
            else:
                raise PermissionDenied(
                    "You do not have permission to view other patients' appointments.")

        else:
            raise PermissionDenied(
                "You do not have permission to view these appointments.")

        return render(request, 'appointments/appointments.html', {
            'appointments': appointments,
            'user_type': user_type,
            'user_id': user_id
        })

    except ObjectDoesNotExist:
        return redirect('index')


@login_required
@permission_required('users.view_user', raise_exception=True)
def list_patients(request):
    if not request.user.groups.filter(name='doctor').exists() and not request.user.is_superuser:
        raise PermissionDenied("You do not have permission to view this page.")
    if request.user.groups.filter(name='doctor').exists():
        appointments = Appointment.objects.filter(
            doctor=request.user).distinct()
    else:
        appointments = Appointment.objects.all()

    return render(request, 'appointments/list_patients.html', {'appointments': appointments})
