from rest_framework.permissions import AllowAny
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from web.appointments.models import Appointment
from django.core.exceptions import PermissionDenied
from django.core.cache import cache
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from .serializers import AppointmentSerializer
from .permissions import IsAdminOnly, IsAdminOrReadOnlyForOthers
from django_filters import rest_framework as filters


class AppointmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Appointment instances.

    Provides different levels of access based on user role:
    - Admin users can view and modify all appointments.
    - Doctors can only view and modify appointments where they are the assigned doctor.
    - Patients can only view and modify appointments where they are the assigned patient.

    Permission Classes:
    - IsAdminOrReadOnlyForOthers: Admin users have full access, while doctors and patients have read-only access.

    Methods:
    - `get_queryset(self)`: Returns a queryset of appointments filtered based on the user's role.
    """
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAdminOrReadOnlyForOthers]

    def get_queryset(self):
        """
        Determines the queryset based on the user's role.
        - Admins: Returns all appointments.
        - Doctors: Returns appointments where the user is the doctor.
        - Patients: Returns appointments where the user is the patient.
        """
        user = self.request.user

        if user.is_superuser:
            queryset = Appointment.objects.all()
        elif user.groups.filter(name='doctor').exists():
            queryset = Appointment.objects.filter(doctor=user)
        elif user.groups.filter(name='patient').exists():
            queryset = Appointment.objects.filter(patient=user)
        else:
            queryset = Appointment.objects.none()

        return queryset


class UserAppointmentListView(generics.ListAPIView):
    """
    API view to list appointments for a specific user, based on user type.

    Caches the result to improve performance. The cache timeout is set to 15 minutes.

    Permission Classes:
    - IsAuthenticated: User must be authenticated to access the view.
    - IsAdminOnly: Only admin users have access.

    Methods:
    - `get_queryset(self)`: Retrieves a cached queryset of appointments or fetches it if not cached.
    - `get(self, request, *args, **kwargs)`: Validates the user type and retrieves the list of appointments.
    """
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated, IsAdminOnly]
    cache_timeout = 60 * 15

    def get_queryset(self):
        """
        Retrieves the queryset from cache or database based on user type and user ID.
        - User type must be either 'doctor' or 'patient'.
        - Raises PermissionDenied if the user type is invalid.

        Caches the queryset for improved performance.
        """
        user_id = self.kwargs.get('user_id')
        user_type = self.kwargs.get('user_type')
        cache_key = f"appointments_{user_id}_{
            user_type}_{self.request.user.id}"
        queryset = cache.get(cache_key)

        if queryset is None:
            if user_type not in ['doctor', 'patient']:
                raise PermissionDenied("Invalid user type.")

            if user_type == 'doctor':
                queryset = Appointment.objects.filter(doctor_id=user_id)
            elif user_type == 'patient':
                queryset = Appointment.objects.filter(patient_id=user_id)

            cache.set(cache_key, queryset, timeout=self.cache_timeout)
        return queryset

    def get(self, request, *args, **kwargs):
        """
        Validates the user type and retrieves the list of appointments.
        - Raises PermissionDenied if the user type is invalid.
        """
        user_type = self.kwargs.get('user_type')
        if user_type not in ['doctor', 'patient']:
            raise PermissionDenied("Invalid user type.")
        return super().get(request, *args, **kwargs)


class CustomAuthToken(ObtainAuthToken):
    """
    Custom view for obtaining authentication tokens.

    Allows any user to request an authentication token by providing their username and password.

    Permission Classes:
    - AllowAny: No authentication required.

    Methods:
    - `post(self, request, *args, **kwargs)`: Validates the user credentials and returns an authentication token along with user ID and email.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Handles token creation for authenticated users.

        Returns:
        - A response containing the token, user ID, and email.
        """
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
