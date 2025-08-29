from django.db import models
from accounts.models import User

class Request(models.Model):
    STATUS_CHOICES = (
        ('pending', 'در انتظار بررسی'),
        ('in_progress', 'در حال پیگیری'),
        ('done', 'انجام شده'),
        ('rejected', 'رد شده'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="requests")
    title = models.CharField(max_length=200)
    type = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    description = models.TextField(blank=True, null=True)
    attachment = models.FileField(upload_to="attachments/", blank=True, null=True)
    response = models.TextField(blank=True, null=True)  # پاسخ کارمند

    def __str__(self):
        return f"{self.title} - {self.user.national_id}"
