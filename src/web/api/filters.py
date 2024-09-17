from web.appointments.models import Appointment
from django_filters import rest_framework as filters


class AppointmentFilter(filters.FilterSet):
    """
    A filter class for filtering `Appointment` instances based on user type and other fields.

    This filter class allows for filtering appointments based on the following criteria:
    - `doctor`: The doctor associated with the appointment.
    - `patient`: The patient associated with the appointment.
    - `scheduled_at`: The scheduled date and time of the appointment.

    Additionally, it provides a custom filter method to filter by user type. Depending on the user's 
    role (admin, doctor, patient), it will filter appointments accordingly.

    Attributes:
        user_type (django_filters.CharFilter): Custom filter method for filtering based on user type.

    Meta:
        model (Appointment): The model to filter.
        fields (list): The fields to filter by.
    """
    user_type = filters.CharFilter(method='filter_by_user_type')

    class Meta:
        model = Appointment
        fields = ['doctor', 'patient', 'scheduled_at']

    def filter_by_user_type(self, queryset, name, value):
        """
        Custom filter method to filter appointments based on user type and user ID.

        This method applies filtering based on whether the user is a superuser, a doctor, or a patient.
        - Superusers can filter by doctor or patient, depending on the `user_type` value.
        - Doctors can only view their own appointments.
        - Patients can only view their own appointments.

        Args:
            queryset (django.db.models.QuerySet): The initial queryset of `Appointment` objects.
            name (str): The name of the filter (in this case, 'user_type').
            value (str): The value to filter by ('doctor' or 'patient').

        Returns:
            django.db.models.QuerySet: The filtered queryset based on the user type and user ID.
        """
        user = self.request.user
        user_id = self.request.query_params.get('user_id')

        if user.is_superuser:
            if value == 'doctor':
                queryset = queryset.filter(doctor=user_id)
            elif value == 'patient':
                queryset = queryset.filter(patient=user_id)
            else:
                queryset = Appointment.objects.none()
        elif user.groups.filter(name='doctor').exists():
            if value == 'doctor' and str(user.id) == user_id:
                queryset = queryset.filter(doctor=user)
            else:
                queryset = Appointment.objects.none()
        elif user.groups.filter(name='patient').exists():
            if value == 'patient' and str(user.id) == user_id:
                queryset = queryset.filter(patient=user)
            else:
                queryset = Appointment.objects.none()
        else:
            queryset = Appointment.objects.none()

        return queryset
