"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# config/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler403, handler400, handler500, handler404
from django.shortcuts import render

def custom_permission_denied_view(request, exception=None):
    return render(request, 'errors/403.html', status=403)

def custom_bad_request_view(request, exception=None):
    return render(request, 'errors/400.html', status=400)

def custom_error_view(request):
    return render(request, 'errors/500.html', status=500)

def custom_404_view(request,exception):
    return render(request, 'errors/500.html', status=404)

handler403 = custom_permission_denied_view
handler400 = custom_bad_request_view
handler500 = custom_error_view
handler404=custom_404_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('web.appointments.urls')),
    path('', include('web.medical_records.urls')),  # This should be present
    path('', include('web.users.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
