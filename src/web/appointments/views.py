from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from .models import Appointment
from web.users.models import User
from django.db.models.functions import TruncDate
from django.utils import timezone
from datetime import datetime, timedelta
# from .forms import DateRangeForm, StatusForm, DoctorNameForm
from django.db.models import Count



@login_required
@permission_required('appointments.view_appointment', raise_exception=True)
def show_appointments(request, user_id, user_type):
    try:
        user = get_object_or_404(User, id=user_id)

        if request.user.is_superuser:
            if user_type=='doctor':
                appointments = Appointment.objects.filter(doctor=user_id).order_by('-scheduled_at')
            else:
                appointments = Appointment.objects.filter(patient=user_id).order_by('-scheduled_at')
        elif request.user.groups.filter(name='doctor').exists() and user_type == 'doctor':
            if request.user == user:
                appointments = Appointment.objects.filter(doctor=request.user).order_by('-scheduled_at')
            else:
                raise PermissionDenied("You do not have permission to view other doctors' appointments.")

        elif request.user.groups.filter(name='patient').exists() and user_type == 'patient':
            if request.user == user:
                appointments = Appointment.objects.filter(patient=request.user).order_by('-scheduled_at')
            else:
                raise PermissionDenied("You do not have permission to view other patients' appointments.")

        else:
            raise PermissionDenied("You do not have permission to view these appointments.")

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
        appointments = Appointment.objects.filter(doctor=request.user).distinct()
    else:
        appointments=Appointment.objects.all()

    return render(request, 'appointments/list_patients.html', {'appointments': appointments})

def get_date_range(start_date, end_date):
    start_date = timezone.make_aware(datetime.combine(datetime.strptime(start_date, '%Y-%m-%d'), datetime.min.time()))
    end_date = timezone.make_aware(datetime.combine(datetime.strptime(end_date, '%Y-%m-%d'), datetime.max.time()))
    return start_date, end_date


@login_required
@permission_required('appointments.view_appointment', raise_exception=True)
def reporting_view(request, user_type):
    appointments_per_day = []
    appointments = []
    status_appointment = []
    doc_name = []

    if request.method == 'POST':
        # Get the date range from the POST data
        from_date = request.POST.get('from')
        till_date = request.POST.get('till')
        status = request.POST.get('status')
        doctor_name = request.POST.get('docname')

        # Validate date range input
        try:
            start_date, end_date = get_date_range(from_date, till_date)
        except ValueError:
            start_date, end_date = None, None

        print(start_date, end_date)
        # Prepare base queryset
        queryset = Appointment.objects.all()

        # Filter by date range if provided
        if start_date and end_date:
            queryset = queryset.filter(scheduled_at__range=(start_date, end_date))

            # Query to get appointments per day
            appointments_per_day = queryset.annotate(
                day=TruncDate('scheduled_at')
            ).values('day').annotate(
                count=Count('pk')
            ).order_by('day')
            print(appointments_per_day)

        # Filter by status if provided
        if status:
            status_appointment = queryset.filter(status=status).order_by('-scheduled_at')

        # Filter by doctor name if provided
        if doctor_name:
            doc_name = queryset.filter(doctor__name__icontains=doctor_name).order_by('-scheduled_at')

        # Filter appointments based on user type and permissions
        if user_type == 'doctor':
            # Add any specific filtering for doctors if needed, otherwise show all appointments
            appointments = queryset.order_by('-scheduled_at')
        else:
            appointments = queryset.order_by('-scheduled_at')

    # Only show appointments if the user has permission or is a superuser
    if not request.user.is_superuser:
        raise PermissionDenied("You do not have permission to view these appointments.")

    return render(request, 'appointments/track.html', {
        'appointments': appointments,
        'appointments_per_day': appointments_per_day,
        'status_appointment': status_appointment,
        'doc_name': doc_name,
        'user_type': user_type,
    })
