# Generated by Django 4.2.5 on 2023-11-26 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crisisManagementAssistant', '0007_cmdoc_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='cmdoc',
            name='extractData',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
