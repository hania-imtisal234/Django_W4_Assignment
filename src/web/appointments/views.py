from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from web.users.models import User
from .models import Appointment

@login_required
def show_appointments(request):
    doctor = User.get_by_id(request.user.id)
    appointments = Appointment.objects.filter(doctor=doctor).order_by('-scheduled_at')
    return render(request, 'appointments/appointments.html', {'appointments': appointments, 'doctor': doctor})

