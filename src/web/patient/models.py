from django.db import models
from django.utils import timezone


class Patient(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female')
    ]
    
    name = models.CharField(max_length=100) 
    email = models.EmailField(unique=True)  
    phone_number = models.CharField(max_length=15)  
    date_of_birth = models.DateField() 
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)  
    created_at = models.DateTimeField(default=timezone.now)  
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"{self.name} ({self.email})"


 

