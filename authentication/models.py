from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    group = models.TextField(blank=True, null=True)
    timeStamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username