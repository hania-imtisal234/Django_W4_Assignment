from django.views.generic import ListView
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from .models import Appointment
from web.users.models import User
from django.db.models.functions import TruncDate
from django.utils import timezone
from datetime import datetime, timedelta
# from .forms import DateRangeForm, StatusForm, DoctorNameForm
from django.db.models import Count




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

