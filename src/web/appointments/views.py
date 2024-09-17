
from django.shortcuts import get_object_or_404

from web.users.models import User
from .models import Appointment
from django.core.exceptions import PermissionDenied
from django.core.cache import cache
from django.views.generic import ListView
from django.core.exceptions import PermissionDenied
from .models import Appointment
from django.db.models.functions import TruncDate
from django.utils import timezone
from datetime import datetime
from django.db.models import Count
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import TemplateView

from .models import Appointment

# class PatientListView(ListView):
#     model = Appointment
#     template_name = 'appointments/list_patients.html'
#     context_object_name = 'appointments'
#     cache_timeout = 60 * 15

#     def get_queryset(self):
#         user = self.request.user
#         cache_key = f"patient_appointments_{user.id}"
#         queryset = cache.get(cache_key)

#         if queryset is None:
#             if not (user.groups.filter(name='doctor').exists() or user.is_superuser):
#                 raise PermissionDenied(
#                     "You do not have permission to view this page.")

#             if user.groups.filter(name='doctor').exists():
#                 queryset = Appointment.objects.filter(doctor=user).distinct()
#             else:
#                 queryset = Appointment.objects.all()

#             cache.set(cache_key, queryset, timeout=self.cache_timeout)

#         return queryset

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return context


class AppointmentListView(ListView):
    template_name = 'appointments/appointments.html'
    context_object_name = 'appointments'
    ordering = '-scheduled_at'
    cache_timeout = 60 * 15  # Cache timeout in seconds (15 minutes)
    paginate_by = 2  # Number of appointments per page

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


class PatientListView(ListView):
    model = Appointment
    template_name = 'appointments/list_patients.html'
    context_object_name = 'appointments'
    paginate_by = 3  # Number of appointments per page

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


class ReportingView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'appointments/track.html'
    permission_required = 'appointments.view_appointment'
    raise_exception = True
    cache_timeout = 300  # Cache timeout in seconds (5 minutes)

    def get_date_range(self, start_date, end_date):
        start_date = timezone.make_aware(datetime.combine(
            datetime.strptime(start_date, '%Y-%m-%d'), datetime.min.time()))
        end_date = timezone.make_aware(datetime.combine(
            datetime.strptime(end_date, '%Y-%m-%d'), datetime.max.time()))
        return start_date, end_date

    def get(self, request, *args, **kwargs):
        return self.render_with_context(request)

    def post(self, request, *args, **kwargs):
        return self.render_with_context(request)

    def render_with_context(self, request):
        user_type = self.kwargs.get('user_type')
        appointments_per_day = []
        appointments = []
        status_appointment = []
        doc_name = []

        # Initialize context
        context = {
            'appointments': appointments,
            'appointments_per_day': appointments_per_day,
            'status_appointment': status_appointment,
            'doc_name': doc_name,
            'user_type': user_type,
        }

        if request.method == 'POST':
            # Get the date range and filters from the POST data
            from_date = request.POST.get('from')
            till_date = request.POST.get('till')
            status = request.POST.get('status')
            doctor_name = request.POST.get('docname')

            # Validate and parse date range input
            try:
                start_date, end_date = self.get_date_range(
                    from_date, till_date)
            except ValueError:
                start_date, end_date = None, None

            # Generate cache key based on filters
            cache_key = f"appointments_{start_date}_{
                end_date}_{status}_{doctor_name}_{user_type}"

            # Check if the data is already cached
            cached_data = cache.get(cache_key)
            if cached_data:
                print("Returning cached data")
                return self.render_to_response(cached_data)

            # Prepare base queryset
            queryset = Appointment.objects.all()

            # Filter by date range if provided
            if start_date and end_date:
                queryset = queryset.filter(
                    scheduled_at__range=(start_date, end_date))

                # Query to get appointments per day
                appointments_per_day = queryset.annotate(
                    day=TruncDate('scheduled_at')
                ).values('day').annotate(count=Count('pk')).order_by('day')

            # Filter by status if provided
            if status:
                status_appointment = queryset.filter(
                    status=status).order_by('-scheduled_at')

            # Filter by doctor name if provided
            if doctor_name:
                doc_name = queryset.filter(
                    doctor__name__icontains=doctor_name).order_by('-scheduled_at')

            # Filter appointments based on user type
            if user_type == 'doctor':
                appointments = queryset.order_by('-scheduled_at')
            else:
                appointments = queryset.order_by('-scheduled_at')

            # Update context after filtering
            context.update({
                'appointments': appointments,
                'appointments_per_day': appointments_per_day,
                'status_appointment': status_appointment,
                'doc_name': doc_name,
            })

            # Cache the result
            cache.set(cache_key, context, timeout=self.cache_timeout)

        return self.render_to_response(context)
