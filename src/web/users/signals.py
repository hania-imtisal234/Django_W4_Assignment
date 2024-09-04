from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.apps import apps

@receiver(post_migrate)
def create_user_groups(sender, **kwargs):
    # Define the groups and permissions
    groups_permissions = {
        'admin': [
            'add_user', 'change_user', 'delete_user', 'view_user',
            'add_appointment', 'change_appointment', 'delete_appointment', 'view_appointment',
            'add_medicalrecord', 'change_medicalrecord', 'delete_medicalrecord', 'view_medicalrecord'
        ],
        'doctor': [
            'view_user', 'view_appointment', 'add_medicalrecord', 'change_medicalrecord', 'view_medicalrecord'
        ],
        'patient': [
            'view_appointment', 'view_medicalrecord'
        ],
    }

    # Ensure content types for models
    user_content_type = ContentType.objects.get_for_model(apps.get_model('users', 'User'))
    appointment_content_type = ContentType.objects.get_for_model(apps.get_model('appointments', 'Appointment'))
    medicalrecord_content_type = ContentType.objects.get_for_model(apps.get_model('medical_records', 'MedicalRecord'))

    # Loop over each group and their permissions
    for group_name, permissions in groups_permissions.items():
        group, created = Group.objects.get_or_create(name=group_name)

        for perm in permissions:
            # Dynamically assign permissions to each group
            model = perm.split('_')[-1]
            if model == 'user':
                content_type = user_content_type
            elif model == 'appointment':
                content_type = appointment_content_type
            elif model == 'medicalrecord':
                content_type = medicalrecord_content_type
            else:
                continue

            # Check if the permission already exists before creating it
            permission = Permission.objects.filter(
                codename=perm,
                content_type=content_type,
            ).first()
            if not permission:
                permission = Permission.objects.create(
                    codename=perm,
                    name=f'Can {perm.replace("_", " ")}',
                    content_type=content_type,
                )
            group.permissions.add(permission)
