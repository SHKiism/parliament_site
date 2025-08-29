# Create your models here.
from django.db import models


class User(models.Model):
    ROLE_CHOICES = (
        ('citizen', 'مردم'),
        ('employee', 'کارمند'),
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    national_id = models.CharField(max_length=10, unique=True)
    phone = models.CharField(max_length=11, unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='citizen')
    is_verified = models.BooleanField(default=False)  # آیا ثبت‌نام کامل کرده؟

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"
