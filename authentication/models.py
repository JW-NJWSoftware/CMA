from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

class CustomUser(AbstractUser):
    group = models.TextField(blank=True, null=True)
    timeStamp = models.DateTimeField(auto_now=True)
    role = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.username
