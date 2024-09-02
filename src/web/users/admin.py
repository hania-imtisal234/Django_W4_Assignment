from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Doctor, Admin
from .forms import CustomUserCreationForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    model = User
    list_display = ('username', 'first_name','last_name','email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username','first_name','last_name', 'email', 'password', 'role')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','first_name','last_name' ,'email', 'role', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email','first_name','last_name')
    ordering = ('email','first_name','last_name')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if obj.role == 'doctor' and not hasattr(obj, 'doctor'):
            Doctor.objects.create(user=obj)
        elif obj.role == 'admin' and not hasattr(obj, 'admin'):
            Admin.objects.create(user=obj)

    def response_add(self, request, obj, post_url_continue=None):
        if obj.role == 'doctor':
            return HttpResponseRedirect(reverse('admin:users_doctor_change', args=[obj.doctor.id]))
        elif obj.role == 'admin':
            return HttpResponseRedirect(reverse('admin:users_admin_change', args=[obj.admin.id]))
        return super().response_add(request, obj, post_url_continue)

admin.site.register(User, CustomUserAdmin)
admin.site.register(Doctor)
admin.site.register(Admin)