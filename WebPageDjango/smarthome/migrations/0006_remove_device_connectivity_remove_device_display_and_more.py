# Generated by Django 5.0.7 on 2024-08-01 10:13

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('smarthome', '0005_delete_pageview'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='device',
            name='connectivity',
        ),
        migrations.RemoveField(
            model_name='device',
            name='display',
        ),
        migrations.RemoveField(
            model_name='device',
            name='image',
        ),
        migrations.RemoveField(
            model_name='device',
            name='processor',
        ),
        migrations.RemoveField(
            model_name='device',
            name='ram',
        ),
        migrations.RemoveField(
            model_name='device',
            name='storage',
        ),
        migrations.AddField(
            model_name='device',
            name='device_type',
            field=models.CharField(choices=[('sensor', 'Sensor'), ('actuator', 'Actuator')], default='Sensor', max_length=255),
        ),
        migrations.AddField(
            model_name='device',
            name='firmware',
            field=models.CharField(default='NAN', max_length=255),
        ),
        migrations.AddField(
            model_name='device',
            name='last_connected',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='device',
            name='manufacturer',
            field=models.CharField(default='NAN', max_length=255),
        ),
        migrations.AddField(
            model_name='sensor',
            name='sensor_type',
            field=models.CharField(default='NAN', max_length=255),
        ),
        migrations.AddField(
            model_name='sensor',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='device',
            name='model',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='device',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='room',
            name='name',
            field=models.CharField(choices=[('salon', 'Salon'), ('cuisine', 'Cuisine'), ('chambre', 'Chambre'), ('salle de bain', 'Salle de bain')], max_length=255),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_guest', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table_name', models.CharField(max_length=255)),
                ('record_id', models.IntegerField()),
                ('field_name', models.CharField(max_length=255)),
                ('old_value', models.TextField()),
                ('new_value', models.TextField()),
                ('updated_at', models.DateTimeField()),
                ('message', models.TextField(blank=True, null=True)),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('value', models.FloatField(default=0)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='smarthome.device')),
            ],
        ),
        migrations.DeleteModel(
            name='Setting',
        ),
    ]
