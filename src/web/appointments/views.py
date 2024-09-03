from .models import Appointment
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from web.users.models import User  # Ensure correct import paths for your models

@login_required
def show_appointments(request, user_id, user_type):
    appointments = []
    doctor = None  

    print(f"user_type: {user_type}")

    try:
        if user_type == 'doctor':
            doctor = User.get_by_id(user_id)
            appointments = Appointment.objects.filter(doctor=doctor).order_by('-scheduled_at')
        else:
            patient = User.get_by_id(user_id)
            appointments = Appointment.objects.filter(patient=patient).order_by('-scheduled_at')
    except User.DoesNotExist:  
        return render(request, '404.html', {'error': 'User not found'})  # Adjust to your 404 page
    
    return render(request, 'appointments/appointments.html', {
        'appointments': appointments,
        'doctor': doctor,  # Doctor will be None if user_type is not 'doctor'
        'user_type': user_type
    })