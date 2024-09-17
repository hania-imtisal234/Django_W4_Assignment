"""
Test cases for authentication and appointment-related views in the web application.

This module includes test cases for:

1. **Custom Authentication Token Tests (`CustomAuthTokenTests`)**:
    - `test_valid_user_authentication`: Tests successful authentication with valid credentials and checks that the token response includes the user ID and email.
    - `test_invalid_user_authentication`: Tests authentication with invalid credentials and expects a bad request response.

2. **User Appointment List View Tests (`UserAppointmentListViewTests`)**:
    - `test_get_appointments_for_doctor`: Tests that a doctor can retrieve their appointments and ensures the correct number of appointments are returned.
    - `test_get_appointments_for_patient`: Tests that a patient can retrieve their appointments and ensures the correct number of appointments are returned.
    - `test_get_appointments_for_invalid_user_type`: Tests the response when an invalid user type is provided and expects a forbidden response.
    - `test_get_appointments_for_unauthenticated_user`: Tests that an unauthenticated user cannot retrieve appointments and expects an unauthorized response.

3. **Appointment View Set Tests (`AppointmentViewSetTests`)**:
    - `test_admin_can_see_all_appointments`: Tests that an admin user can view all appointments and ensures the correct number of appointments are returned.
    - `test_doctor_can_see_their_appointments`: Tests that a doctor can view their own appointments and ensures the correct number of appointments are returned.
    - `test_patient_can_see_their_appointments`: Tests that a patient is forbidden from viewing their appointments and expects a forbidden response.
    - `test_unauthenticated_user_cannot_see_appointments`: Tests that an unauthenticated user cannot access appointments and expects an unauthorized response.

Each test case uses the `APITestCase` class from the Django REST framework to simulate requests and validate responses based on user roles and authentication status. The `setUp` method initializes test data, including users, appointments, and groups, to ensure a consistent testing environment.
"""


from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User, Group
from web.appointments.models import Appointment
from rest_framework.authtoken.models import Token


class CustomAuthTokenTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass', email='testuser@example.com')
        self.client = APITestCase()

    def test_valid_user_authentication(self):
        data = {
            'username': 'testuser',
            'password': 'testpass'
        }
        response = self.client.post('/api-token-auth/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['user_id'], self.user.pk)
        self.assertEqual(response.data['email'], self.user.email)

    def test_invalid_user_authentication(self):
        data = {
            'username': 'wronguser',
            'password': 'wrongpass'
        }
        response = self.client.post('/api-token-auth/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserAppointmentListViewTests(APITestCase):

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin', password='adminpass', email='admin@example.com')
        self.doctor_user = User.objects.create_user(
            username='doctor', password='doctorpass', email='doctor@example.com')
        self.patient_user = User.objects.create_user(
            username='patient', password='patientpass', email='patient@example.com')

        # Create appointments
        self.appointment1 = Appointment.objects.create(
            doctor=self.doctor_user, patient=self.patient_user)
        self.appointment2 = Appointment.objects.create(
            doctor=self.doctor_user, patient=self.patient_user)

        self.client = APITestCase()

    def test_get_appointments_for_doctor(self):
        self.client.force_authenticate(user=self.doctor_user)
        response = self.client.get(reverse('user_appointments', kwargs={
                                   'user_id': self.doctor_user.pk, 'user_type': 'doctor'}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_appointments_for_patient(self):
        self.client.force_authenticate(user=self.patient_user)
        response = self.client.get(reverse('user_appointments', kwargs={
                                   'user_id': self.patient_user.pk, 'user_type': 'patient'}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_appointments_for_invalid_user_type(self):
        self.client.force_authenticate(user=self.patient_user)
        response = self.client.get(reverse('user_appointments', kwargs={
                                   'user_id': self.patient_user.pk, 'user_type': 'invalid'}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_appointments_for_unauthenticated_user(self):
        response = self.client.get(reverse('user_appointments', kwargs={
                                   'user_id': self.doctor_user.pk, 'user_type': 'doctor'}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AppointmentViewSetTests(APITestCase):

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin', password='adminpass', email='admin@example.com')
        self.doctor_user = User.objects.create_user(
            username='doctor', password='doctorpass', email='doctor@example.com')
        self.patient_user = User.objects.create_user(
            username='patient', password='patientpass', email='patient@example.com')

        # Create groups and add users to groups
        doctor_group = Group.objects.create(name='doctor')
        patient_group = Group.objects.create(name='patient')
        self.doctor_user.groups.add(doctor_group)
        self.patient_user.groups.add(patient_group)

        # Create appointments
        self.appointment1 = Appointment.objects.create(
            doctor=self.doctor_user, patient=self.patient_user)
        self.appointment2 = Appointment.objects.create(
            doctor=self.doctor_user, patient=self.patient_user)

        self.client = APITestCase()

    def test_admin_can_see_all_appointments(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get('/appointments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_doctor_can_see_their_appointments(self):
        self.client.force_authenticate(user=self.doctor_user)
        response = self.client.get('/appointments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_patient_can_see_their_appointments(self):
        self.client.force_authenticate(user=self.patient_user)
        response = self.client.get('/appointments/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_user_cannot_see_appointments(self):
        response = self.client.get('/appointments/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
