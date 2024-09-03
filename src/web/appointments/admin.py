from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Appointment
from web.users.models import User


class AppointmentAdmin(admin.ModelAdmin):
    search_fields = ['doctor__name', 'patient__name', 'scheduled_at']
    list_filter = ['scheduled_at', 'created_at']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "doctor":
            try:
                doctor_group = Group.objects.get(name='doctor')
                kwargs["queryset"] = User.objects.filter(groups=doctor_group)
            except Group.DoesNotExist:
                kwargs["queryset"] = User.objects.none()

        elif db_field.name == "patient":
            try:
                patient_group = Group.objects.get(name='patient')
                kwargs["queryset"] = User.objects.filter(groups=patient_group)
            except Group.DoesNotExist:
                kwargs["queryset"] = User.objects.none()

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Appointment, AppointmentAdmin)
