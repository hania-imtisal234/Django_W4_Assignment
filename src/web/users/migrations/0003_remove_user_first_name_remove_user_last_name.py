# Generated by Django 5.1 on 2024-09-04 00:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='last_name',
        ),
    ]
