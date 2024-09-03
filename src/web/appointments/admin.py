from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Appointment
from web.users.models import User


class AppointmentAdmin(admin.ModelAdmin):
    # Add search fields and filters
    search_fields = ['doctor__name', 'patient__name', 'scheduled_at']
    list_filter = ['scheduled_at', 'created_at']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Restrict doctor field to users in the doctor group
        if db_field.name == "doctor":
            try:
                doctor_group = Group.objects.get(name='doctor')
                kwargs["queryset"] = User.objects.filter(groups=doctor_group)
            except Group.DoesNotExist:
                kwargs["queryset"] = User.objects.none()

        # Restrict patient field to users in the patient group
        elif db_field.name == "patient":
            try:
                patient_group = Group.objects.get(name='patient')
                kwargs["queryset"] = User.objects.filter(groups=patient_group)
            except Group.DoesNotExist:
                kwargs["queryset"] = User.objects.none()

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Appointment, AppointmentAdmin)
