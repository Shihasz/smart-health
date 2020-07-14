from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_patient = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)


DISTRICTS = [
    ('AL', 'Alappuzha'),
    ('ER', 'Ernakulam'),
    ('ID', 'Idukki'),
    ('KN', 'Kannur'),
    ('KS', 'Kasargod'),
    ('KZ', 'Kozhikode'),
    ('KL', 'Kollam'),
    ('KT', 'Kottayam'),
    ('MA', 'Malappuram'),
    ('PL', 'Palakkad'),
    ('PT', 'Pathanamthitta'),
    ('TV', 'Thiruvnanthapuram'),
    ('TS', 'Thrissur'),
    ('WA', 'Wayanad')
]


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    age = models.PositiveIntegerField()
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female')
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+ve'),
        ('A-', 'A-ve'),
        ('B+', 'B+ve'),
        ('B-', 'B-ve'),
        ('O+', 'O+ve'),
        ('O-', 'O-ve'),
        ('AB+', 'AB+ve'),
        ('AB-', 'AB-ve')
    ]
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    place = models.CharField(max_length=100, choices=DISTRICTS)

    def __str__(self):
        return self.user.username


class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    place = models.CharField(max_length=100, choices=DISTRICTS)

    def __str__(self):
        return self.user.username


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='patient_id')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctor_id')
    date = models.DateField()
    status = models.BooleanField(default=False)


class Disease(models.Model):
    name = models.CharField(max_length=50)
    department = models.ManyToManyField(Department, null=True)
    treatments = models.CharField(max_length=5000, null=True)
    remedies = models.CharField(max_length=5000, null=True)

    def __str__(self):
        return self.name