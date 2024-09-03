from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from .models import Appointment
from web.users.models import User

@login_required
@permission_required('appointments.view_appointment', raise_exception=True)
def show_appointments(request, user_id, user_type):
    try:
        # Fetch the user based on user_id
        user = get_object_or_404(User, id=user_id)

        # Admin: View all appointments
        if request.user.is_superuser:
            appointments = Appointment.objects.all().order_by('-scheduled_at')

        # Doctor: View their own appointments
        elif request.user.groups.filter(name='doctor').exists() and user_type == 'doctor':
            if request.user == user:
                appointments = Appointment.objects.filter(doctor=request.user).order_by('-scheduled_at')
            else:
                raise PermissionDenied("You do not have permission to view other doctors' appointments.")

        # Patient: View their own appointments
        elif request.user.groups.filter(name='patient').exists() and user_type == 'patient':
            if request.user == user:
                appointments = Appointment.objects.filter(patient=request.user).order_by('-scheduled_at')
            else:
                raise PermissionDenied("You do not have permission to view other patients' appointments.")

        # If the user does not have permission
        else:
            raise PermissionDenied("You do not have permission to view these appointments.")

        return render(request, 'appointments/appointments.html', {
            'appointments': appointments,
            'user_type': user_type,
            'user_id': user_id
        })

    except ObjectDoesNotExist:
        # Django will handle the 404 error if user is not found
        return redirect('index')
