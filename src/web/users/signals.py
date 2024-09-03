from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.apps import apps

@receiver(post_migrate)
def create_user_groups(sender, **kwargs):
    # Define the groups and permissions
    groups = {
        'admin': ['add_user', 'change_user', 'delete_user', 'view_user'],
        'doctor': ['view_user'],
        'patient': ['view_user'],
    }

    for group_name, permissions in groups.items():
        group, created = Group.objects.get_or_create(name=group_name)
        for perm in permissions:
            # Ensure the permission exists
            content_type = ContentType.objects.get_for_model(apps.get_model('auth', 'User'))
            permission, created = Permission.objects.get_or_create(
                codename=perm,
                name=f'Can {perm.replace("_", " ")} user',
                content_type=content_type,
            )
            group.permissions.add(permission)
