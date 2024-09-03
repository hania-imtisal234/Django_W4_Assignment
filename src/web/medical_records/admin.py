from django.contrib import admin
from django.contrib.auth.models import Group
from .models import MedicalRecord
from web.users.models import User


class MedicalRecordAdmin(admin.ModelAdmin):
    search_fields = ['patient__name', 'doctor__name', 'diagnosis', 'treatment']
    list_filter = ['created_at', 'updated_at']

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


admin.site.register(MedicalRecord, MedicalRecordAdmin)
