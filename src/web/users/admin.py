from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from .forms import CustomUserCreationForm

class UserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm  

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'name', 'phone_number', 'date_of_birth', 'address','gender', 'specialization', 'password1', 'password2', 'groups'),
        }),
    )

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('name', 'email', 'phone_number', 'address','date_of_birth', 'gender', 'specialization')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    search_fields = ('username', 'email', 'name', 'groups__name')
    list_filter = ('groups', 'specialization')

    def groups_names(self, obj):
        return ", ".join(group.name for group in obj.groups.all())
    groups_names.short_description = 'Groups'

    list_display = ('username', 'name', 'email', 'groups_names')

admin.site.register(User, UserAdmin)
