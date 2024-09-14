# Generated by Django 5.0.7 on 2024-09-11 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smarthome', '0013_outlet'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='temperature',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='device',
            name='device_type',
            field=models.CharField(choices=[('lampe', 'Lampe'), ('plug', 'Plug'), ('clima', 'Clima')], default='lampe', max_length=255),
        ),
    ]