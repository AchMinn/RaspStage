# Generated by Django 5.0.7 on 2024-07-29 21:35

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smarthome', '0002_device_connectivity_device_display_device_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='room',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]