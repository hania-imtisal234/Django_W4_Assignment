from django.contrib import admin
from django.urls import path
from .views import login_view, logout_view, homepage_view

urlpatterns = [
    path('',homepage_view, name='index'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('admin/', admin.site.urls),
]
