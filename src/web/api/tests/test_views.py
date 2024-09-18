# """
# # Test cases for authentication and appointment-related views in the web application.

# # This module includes test cases for:

# # 1. **Custom Authentication Token Tests (`CustomAuthTokenTests`)**:
# #     - `test_valid_user_authentication`: Tests successful authentication with valid credentials and checks that the token response includes the user ID and email.
# #     - `test_invalid_user_authentication`: Tests authentication with invalid credentials and expects a bad request response.

# # 2. **User Appointment List View Tests (`UserAppointmentListViewTests`)**:
# #     - `test_get_appointments_for_doctor`: Tests that a doctor can retrieve their appointments and ensures the correct number of appointments are returned.
# #     - `test_get_appointments_for_patient`: Tests that a patient can retrieve their appointments and ensures the correct number of appointments are returned.
# #     - `test_get_appointments_for_invalid_user_type`: Tests the response when an invalid user type is provided and expects a forbidden response.
# #     - `test_get_appointments_for_unauthenticated_user`: Tests that an unauthenticated user cannot retrieve appointments and expects an unauthorized response.

# # 3. **Appointment View Set Tests (`AppointmentViewSetTests`)**:
# #     - `test_admin_can_see_all_appointments`: Tests that an admin user can view all appointments and ensures the correct number of appointments are returned.
# #     - `test_doctor_can_see_their_appointments`: Tests that a doctor can view their own appointments and ensures the correct number of appointments are returned.
# #     - `test_patient_can_see_their_appointments`: Tests that a patient is forbidden from viewing their appointments and expects a forbidden response.
# #     - `test_unauthenticated_user_cannot_see_appointments`: Tests that an unauthenticated user cannot access appointments and expects an unauthorized response.

# # Each test case uses the `APITestCase` class from the Django REST framework to simulate requests and validate responses based on user roles and authentication status. The `setUp` method initializes test data, including users, appointments, and groups, to ensure a consistent testing environment.
# # """


# from django.test import TransactionTestCase
# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APITestCase
# from django.contrib.auth.models import User, Group
# from web.appointments.models import Appointment
# from rest_framework.authtoken.models import Token
# from django.contrib.auth import get_user_model
# from django.utils import timezone

# User = get_user_model()

# # class AccountTests(APITestCase):
# #     def test_create_account(self):
# #         """
# #         Ensure we can create a new account object.
# #         """
# #         url = reverse('account-list')
# #         data = {'name': 'DabApps'}
# #         response = self.client.post(url, data, format='json')
# #         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
# #         self.assertEqual(Account.objects.count(), 1)
# #         self.assertEqual(Account.objects.get().name, 'DabApps')


# class AppointmentTests(APITestCase):
#     def setUp(self):
#         """
#         Create test users for doctor and patient.
#         """
#         self.doctor = User.objects.create_user(
#             username='doctor', password='testpassword')
#         self.patient = User.objects.create_user(
#             username='patient', password='testpassword')

#     def test_create_appointment(self):
#         """
#         Ensure we can create a new appointment object.
#         """
#         url = reverse(
#             'appointment-list')  # Adjust this to match the URL name for the appointment list
#         data = {
#             'doctor': self.doctor.id,  # Use the ID of the doctor user
#             'patient': self.patient.id,  # Use the ID of the patient user
#             # Use the current time or a fixed time
#             'scheduled_at': timezone.now().isoformat(),
#         }
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Appointment.objects.count(), 1)
#         appointment = Appointment.objects.get()
#         self.assertEqual(appointment.doctor, self.doctor)
#         self.assertEqual(appointment.patient, self.patient)
#         self.assertEqual(appointment.scheduled_at, timezone.make_aware(
#             timezone.datetime.fromisoformat(data['scheduled_at'])))
# # class CustomAuthTokenTests(APITestCase):
# #     def setUp(self):
# #         """
# #         Set up a test user and token.
# #         """
# #         self.username = 'superadmin'
# #         self.password = 'admin7890'
# #         self.user = User.objects.create_user(
# #             username=self.username, password=self.password)
# #         self.token = Token.objects.create(user=self.user)
# #         self.url = '/loginAuth/'

# #     def test_valid_user_authentication(self):
# #         """
# #         Test valid user authentication.
# #         """
# #         data = {
# #             'username': self.username,
# #             'password': self.password
# #         }
# #         response = self.client.post(self.url, data, format='json')
# #         self.assertEqual(response.status_code, status.HTTP_200_OK)
# #         try:
# #             response_data = response.json()
# #         except ValueError:
# #             self.fail("Response content is not valid JSON")
# #         self.assertIn('token', response_data)
# #         self.assertEqual(response_data['token'], self.token.key)

# # class CustomAuthTokenTests(APITestCase):
# #     def setUp(self):
# #         self.username = 'superadmin'
# #         self.password = 'admin7890'
# #         self.user = User.objects.create_user(
# #             username=self.username, password=self.password)
# #         self.token = Token.objects.create(user=self.user)
# #         self.url = '/api/loginAuth/'  # Match the URL defined in urls.py

# #     def test_valid_user_authentication(self):
# #         data = {
# #             'username': self.username,
# #             'password': self.password
# #         }
# #         response = self.client.post(self.url, data, format='json')

# #         self.assertEqual(response.status_code, status.HTTP_200_OK)

# #         try:
# #             response_data = response.json()
# #         except ValueError:
# #             self.fail("Response content is not valid JSON")

# #         self.assertIn('token', response_data)
# #         self.assertEqual(response_data['token'], self.token.key)

# #     def test_invalid_user_authentication(self):
# #         data = {
# #             'username': 'wronguser',
# #             'password': 'wrongpass'
# #         }
# #         response = self.client.post(self.url, data, format='json')

# #         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

# # class UserAppointmentListViewTests(APITestCase):

# #     def setUp(self):
# #         self.admin_user = User.objects.create_superuser(
# #             username='admin', password='adminpass', email='admin@example.com')
# #         self.doctor_user = User.objects.create_user(
# #             username='doctor', password='doctorpass', email='doctor@example.com')
# #         self.patient_user = User.objects.create_user(
# #             username='patient', password='patientpass', email='patient@example.com')

# #         # Create appointments
# #         self.appointment1 = Appointment.objects.create(
# #             doctor=self.doctor_user, patient=self.patient_user)
# #         self.appointment2 = Appointment.objects.create(
# #             doctor=self.doctor_user, patient=self.patient_user)

# #     def test_get_appointments_for_doctor(self):
# #         self.client.force_authenticate(user=self.doctor_user)
# #         response = self.client.get(reverse('user_appointments', kwargs={
# #                                    'user_id': self.doctor_user.pk, 'user_type': 'doctor'}))
# #         self.assertEqual(response.status_code, status.HTTP_200_OK)
# #         self.assertEqual(len(response.data), 2)

# #     def test_get_appointments_for_patient(self):
# #         self.client.force_authenticate(user=self.patient_user)
# #         response = self.client.get(reverse('user_appointments', kwargs={
# #                                    'user_id': self.patient_user.pk, 'user_type': 'patient'}))
# #         self.assertEqual(response.status_code, status.HTTP_200_OK)
# #         self.assertEqual(len(response.data), 2)

# #     def test_get_appointments_for_invalid_user_type(self):
# #         self.client.force_authenticate(user=self.patient_user)
# #         response = self.client.get(reverse('user_appointments', kwargs={
# #                                    'user_id': self.patient_user.pk, 'user_type': 'invalid'}))
# #         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# #     def test_get_appointments_for_unauthenticated_user(self):
# #         response = self.client.get(reverse('user_appointments', kwargs={
# #                                    'user_id': self.doctor_user.pk, 'user_type': 'doctor'}))
# #         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# # class AppointmentViewSetTests(TransactionTestCase):

# #     def setUp(self):
# #         self.admin_user = User.objects.create_superuser(
# #             username='admin', password='adminpass', email='admin@example.com')
# #         self.doctor_user = User.objects.create_user(
# #             username='doctor', password='doctorpass', email='doctor@example.com')
# #         self.patient_user = User.objects.create_user(
# #             username='patient', password='patientpass', email='patient@example.com')

# #         # Create groups and add users to groups
# #         doctor_group = Group.objects.create(name='doctor')
# #         patient_group = Group.objects.create(name='patient')
# #         self.doctor_user.groups.add(doctor_group)
# #         self.patient_user.groups.add(patient_group)

# #         # Create appointments
# #         self.appointment1 = Appointment.objects.create(
# #             doctor=self.doctor_user, patient=self.patient_user)
# #         self.appointment2 = Appointment.objects.create(
# #             doctor=self.doctor_user, patient=self.patient_user)

# #         self.client = self.client

# #     def test_admin_can_see_all_appointments(self):
# #         self.client.force_authenticate(user=self.admin_user)
# #         response = self.client.get('/appointments/')
# #         self.assertEqual(response.status_code, status.HTTP_200_OK)
# #         self.assertEqual(len(response.data), 2)


from django.test import SimpleTestCase
from django.urls import reverse, resolve
from rest_framework.test import APITestCase, APIClient
from web.api.views import AppointmentViewSet
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import get_user_model


class ApiurlTests(SimpleTestCase):

    def test_get_appointments_is_Resolved(self):
        url = reverse('appointment-list')
        print(resolve(url).func)
        self.assertEqual(resolve(url).func.cls, AppointmentViewSet)


class AppointmentAPIViewTests(APITestCase):
    appointments_urls = reverse('appointment-list')

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username="admin", password="admin7890")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token' + self.token.key)

    def tearDown(self):
        pass

    def test_get_appointments_authenticated(self):
        response = self.client.get(self.appointments_urls)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_appointments_un_authenticated(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.get(self.appointments_urls)
        self.assertEqual(response.status_code, 401)

    def test_post_appointments_authenticated(self):
        data = {
            "doctor": 1,
            "patient": 2,
            "scheduled_at": "2024-09-13 09:21:51+00:00",
            "create_at": "2024-09-13 09:21:51+00:00",
        }

        response = self.client.post(
            self.appointments_urls, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
