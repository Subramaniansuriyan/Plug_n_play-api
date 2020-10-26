from django.db import models
from django.contrib.auth.models import User


class Otp(models.Model):
    otp = models.CharField(max_length=6)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    otp_for = models.CharField(max_length=13,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
