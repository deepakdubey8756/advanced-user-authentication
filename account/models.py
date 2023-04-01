from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    token = models.CharField(max_length=250, default="None")
    isVerified = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.user.username