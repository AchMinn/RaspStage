# Generated by Django 5.0.7 on 2024-07-31 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smarthome', '0003_room_created_at_room_updated_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='PageView',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=255)),
                ('view_count', models.IntegerField(default=0)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]