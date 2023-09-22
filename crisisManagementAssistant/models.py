from django.conf import settings
from django.db import models
from django.urls import reverse
from django.contrib import admin
from django.utils.text import slugify
from ResilienceAI.utils import unique_slugify

User = settings.AUTH_USER_MODEL

class CMDoc(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    fileName = models.CharField(default="", max_length=120)
    desc = models.TextField(default="")
    slug = models.SlugField(max_length=50, blank=True, null=True)
    #file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('id',)

    def save(self, *args, **kwargs):
        slug = "%s" % (self.fileName)
        unique_slugify(self, slug)
        super(CMDoc, self).save(**kwargs)

    def get_absolute_url(self):
        return reverse("view_file", kwargs={"slug": self.slug})
        #return f'view/{self.slug}'
