from django.db import models
from django.utils import timezone

class User(models.Model):
    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(auto_now=True)

class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otp_records')  # Example related_name
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return (timezone.now() - self.created_at).seconds < 300  # OTP is valid for 5 minutes
