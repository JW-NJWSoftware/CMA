# Generated by Django 4.2.5 on 2023-09-22 10:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crisisManagementAssistant', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cmdoc',
            name='file',
        ),
    ]
