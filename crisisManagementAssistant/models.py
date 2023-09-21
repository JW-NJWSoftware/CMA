from django.db import models


class CMDoc(models.Model):
    fileName = models.TextField(default="")
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('id',)
