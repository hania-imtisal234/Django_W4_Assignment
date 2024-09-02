from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from web.users.models import Doctor
from web.appointments.models import Appointment
from web.patient.models import Patient

@login_required
def show_appointments(request):
    doctor = get_object_or_404(Doctor, user=request.user)
    appointments = Appointment.objects.filter(doctor=doctor).order_by('-scheduled_at')
    return render(request, 'appointments/appointments.html', {'appointments': appointments, 'doctor': doctor})

