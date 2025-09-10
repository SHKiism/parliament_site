# Create your models here.
from django.db import models


class Citizen(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    national_id = models.CharField(max_length=10, unique=True)
    phone = models.CharField(max_length=11, unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.national_id}, {self.phone})"


class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    national_id = models.CharField(max_length=10, unique=True)
    phone = models.CharField(max_length=11, unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.national_id}, {self.phone})"
