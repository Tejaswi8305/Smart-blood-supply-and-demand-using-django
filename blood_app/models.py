from django.db import models
from django.contrib.auth.models import User

class Donor(models.Model):
    name = models.CharField(max_length=100)
    blood_group = models.CharField(max_length=5)
    phone = models.CharField(max_length=15)
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Hospital(models.Model):
    hospital_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)

    def __str__(self):
        return self.hospital_name


# models.py
class BloodRequest(models.Model):
    hospital_name = models.CharField(max_length=100)
    blood_group = models.CharField(max_length=10)
    units_needed = models.IntegerField()

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')


class BloodStock(models.Model):
    blood_group = models.CharField(max_length=5)
    units_available = models.IntegerField()

    def __str__(self):
        return self.blood_group
    
class UserProfile(models.Model):

    ROLE_CHOICES = (
        ('admin','Admin'),
        ('donor','Donor'),
        ('hospital','Hospital')
    )

    user = models.OneToOneField(User,on_delete=models.CASCADE)
    role = models.CharField(max_length=20,choices=ROLE_CHOICES)

    def __str__(self):
        return self.user.username