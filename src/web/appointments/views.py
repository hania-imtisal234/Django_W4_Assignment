from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Appointment
from django.shortcuts import get_object_or_404


@login_required
def show_appointments(request,doctor):
    obj = get_object_or_404(Appointment, doctor = doctor)

    return render(request,'appointments/appointments.html')
