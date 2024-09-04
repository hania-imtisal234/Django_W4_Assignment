from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.shortcuts import get_object_or_404


class User(AbstractUser):
    first_name=None
    last_name=None
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    address=models.CharField(max_length=50,blank=True,null=True)

    #field specific to doctor
    specialization = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.is_superuser:
            admin_group, created = Group.objects.get_or_create(name='admin')
            self.groups.add(admin_group)

    @classmethod
    def get_doctors(cls):
        return cls.objects.filter(groups__name='doctor')

    @classmethod
    def get_patients(cls):
        return cls.objects.filter(groups__name='patient')

    @classmethod
    def get_by_id(cls, user_id):
        return get_object_or_404(cls, id=user_id)
