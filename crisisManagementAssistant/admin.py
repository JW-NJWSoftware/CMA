from django.contrib import admin

# Register your models here.
from .models import CMDoc

class CMDocAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'fileName', 'slug', 'timestamp']
    search_fields = ['fileName', 'user']

admin.site.register(CMDoc, CMDocAdmin)