# Generated by Django 4.2.5 on 2024-01-21 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_alter_customuser_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='settings',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
    ]
