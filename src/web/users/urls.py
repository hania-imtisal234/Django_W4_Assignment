from django.contrib import admin
from django.urls import path
from .views import login_view, logout_view, homepage_view, doctor_detail

urlpatterns = [
    path('',homepage_view, name='index'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('admin/', admin.site.urls),
    path('<int:doctor_id>/detail/',doctor_detail,name='detail')
]
