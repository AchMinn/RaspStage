# Generated by Django 5.0.7 on 2024-09-11 08:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smarthome', '0012_remove_device_firmware_remove_device_manufacturer_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Outlet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=False)),
                ('outlet_number', models.PositiveIntegerField()),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='outlets', to='smarthome.device')),
            ],
            options={
                'unique_together': {('device', 'outlet_number')},
            },
        ),
    ]
