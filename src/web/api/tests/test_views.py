from django.test import SimpleTestCase
from django.urls import reverse, resolve
from rest_framework.test import APITestCase, APIClient
from web.api.views import AppointmentViewSet
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import get_user_model


class ApiurlTests(SimpleTestCase):
    """
    Unit tests for testing URL resolution in the API.

    Methods:
    - test_get_appointments_is_Resolved: Tests whether the URL for fetching appointment data resolves to the correct view.
    """

    def test_get_appointments_is_Resolved(self):
        """
        Tests if the 'appointment-list' URL correctly resolves to the AppointmentViewSet.
        """
        url = reverse('appointment-list')
        print(resolve(url).func)
        self.assertEqual(resolve(url).func.cls, AppointmentViewSet)


class AppointmentAPIViewTests(APITestCase):
    """
    API tests for AppointmentViewSet operations: authentication, retrieval, and creation of appointments.

    Methods:
    - setUp: Sets up user authentication before each test case.
    - tearDown: Cleans up resources after each test case.
    - test_get_appointments_authenticated: Tests authenticated access to the appointment list.
    - test_get_appointments_un_authenticated: Tests unauthenticated access to the appointment list.
    - test_post_appointments_authenticated: Tests authenticated creation of new appointments.
    """
    appointments_urls = reverse('appointment-list')

    def setUp(self):
        """
        Sets up the test client with an authenticated user and token for testing.
        """
        User = get_user_model()
        self.user = User.objects.create_user(
            username="admin", password="admin7890")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def tearDown(self):
        """
        Cleans up after each test case. Currently no specific resources to clean up.
        """
        pass

    def test_get_appointments_authenticated(self):
        """
        Tests that an authenticated user can successfully retrieve a list of appointments.
        Expects a 200 OK response.
        """
        response = self.client.get(self.appointments_urls)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_appointments_un_authenticated(self):
        """
        Tests that an unauthenticated user cannot access the appointment list.
        Expects a 401 Unauthorized response.
        """
        self.client.force_authenticate(user=None, token=None)
        response = self.client.get(self.appointments_urls)
        self.assertEqual(response.status_code, 401)

    def test_post_appointments_authenticated(self):
        """
        Tests that an authenticated user can create a new appointment.
        Expects a 201 Created response.
        """
        data = {
            "doctor": 1,
            "patient": 2,
            "scheduled_at": "2024-09-13 09:21:51+00:00",
            "create_at": "2024-09-13 09:21:51+00:00",
        }

        response = self.client.post(
            self.appointments_urls, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
