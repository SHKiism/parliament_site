from django.db import models
from accounts.models import Citizen


class Request(models.Model):
    STATUS_CHOICES = (
        ('pending', 'در انتظار بررسی'),
        ('in_progress', 'در حال پیگیری'),
        ('done', 'انجام شده'),
        ('rejected', 'رد شده'),
    )
    TYPE_CHOICES = (
        ('پیشنهاد', 'پیشنهاد'),
        ('انتقاد', 'انتقاد'),
        ('ملاقات', 'ملاقات'),
        ('شکایت', 'شکایت'),
    )
    citizen = models.ForeignKey(Citizen, on_delete=models.CASCADE, related_name="requests")
    title = models.CharField(max_length=200)
    request_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    description = models.TextField(blank=True, null=True)
    attachment = models.FileField(upload_to="attachments/", blank=True, null=True)
    response = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.citizen.national_id}"
