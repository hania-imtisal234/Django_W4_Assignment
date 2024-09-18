from django.urls import path

from .views import AppointmentViewSet, CustomAuthToken,  UserAppointmentListView

appointment_list = AppointmentViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

appointment_detail = AppointmentViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

user_appointments = UserAppointmentListView.as_view()
urlpatterns = [
    path('loginAuth', CustomAuthToken.as_view(), name='login'),
    path('appointments/', appointment_list, name='appointment-list'),
    path('appointments/<int:pk>/', appointment_detail, name='appointment-detail'),
    path('appointments/<str:user_type>/<int:user_id>/',
         user_appointments, name='show_user_appointments'),
]
