from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler403, handler400, handler500, handler404
from django.shortcuts import render
from web.users.views import HomePageView
import debug_toolbar

from web.users.views import HomePageView


def custom_permission_denied_view(request, exception=None):
    return render(request, 'errors/403.html', status=403)


def custom_bad_request_view(request, exception=None):
    return render(request, 'errors/400.html', status=400)


def custom_error_view(request):
    return render(request, 'errors/500.html', status=500)


def custom_404_view(request, exception):
    return render(request, 'errors/404.html', status=404)


handler403 = custom_permission_denied_view
handler400 = custom_bad_request_view
handler500 = custom_error_view
handler404 = custom_404_view

urlpatterns = [
    path('admin/', admin.site.urls, name='admin_site'),
    path('appointments/', include('web.appointments.urls')),
    path('medical_records/', include('web.medical_records.urls')),
    path('users/', include('web.users.urls')),
    path('', HomePageView.as_view(), name='index'),
    path('__debug__/', include(debug_toolbar.urls))

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
