from django.conf import settings
from django.db import models
from django.urls import reverse
from django.contrib import admin
from django.utils.text import slugify
from ResilienceAI.utils import unique_slugify

class CMDoc(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE)
    fileName = models.CharField(default="", max_length=120)
    desc = models.TextField(default="")
    slug = models.SlugField(max_length=50, blank=True, null=True)
    file = models.FileField(upload_to='cmdocs/', default="")
    timestamp = models.DateTimeField(auto_now_add=True)
    extractData = models.JSONField(blank=True, null=True)

    class Meta:
        ordering = ('id',)

    def save(self, *args, **kwargs):
        slug = "%s" % (self.fileName)
        unique_slugify(self, slug)
        super(CMDoc, self).save(**kwargs)

    def get_absolute_url(self):
        return reverse("view_file", kwargs={"slug": self.slug})
    
    def get_download_url(self):
        return reverse("download_file", kwargs={"file_id": self.id})

    def get_delete_url(self):
        return reverse("delete_file", kwargs={"file_id": self.id})