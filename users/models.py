from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    image = models.ImageField(null=True, blank=True, upload_to="profile/")
    age = models.IntegerField(default=20)

    def __str__(self):
        return f"{self.user.username} - {self.age}"
