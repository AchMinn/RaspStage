# Generated by Django 5.0.7 on 2024-08-01 10:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smarthome', '0007_delete_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='room',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='sensor',
            name='timestamp',
        ),
    ]