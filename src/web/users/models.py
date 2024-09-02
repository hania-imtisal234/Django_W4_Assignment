from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField


class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('doctor', 'Doctor'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES ,default='admin')
    first_name = CharField(max_length=10,null=False)
    last_name=CharField(max_length=10,null=True)
    def __str__(self):
        return self.username
    
    def get_full_name(self):
        return self.first_name+' '+self.last_name

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.user.get_full_name()

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.get_full_name()
