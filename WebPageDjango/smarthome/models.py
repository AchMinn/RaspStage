from django.db import models
from django.utils.timezone import now
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings

class Room(models.Model):
    name = models.CharField(max_length=255, choices=[
        ('salon', 'Salon'), ('cuisine', 'Cuisine'),
        ('chambre', 'Chambre'), ('salle de bain', 'Salle de bain')
    ])
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def device_count(self):
        return self.devices.count()

class Device(models.Model):
    name = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    manufacturer = models.CharField(max_length=255, default="NAN")
    firmware = models.CharField(max_length=255, default="NAN")
    last_connected = models.DateTimeField(default=timezone.now)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, related_name='devices')
    is_active = models.BooleanField(default=False)
    device_type = models.CharField(max_length=255, choices=[
        ('lampe', 'Lampe'), ('plug', 'Plug')
    ],default="Lampe")

    def __str__(self):
        return self.name

class Sensor(models.Model):
    name = models.CharField(max_length=100)
    sensor_type = models.CharField(max_length=255, default="NAN")
    description = models.TextField(null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, related_name='sensors')
    value = models.FloatField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Measurement(models.Model):
    name = models.CharField(max_length=100)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    last_updated = models.DateTimeField(auto_now=True)
    value = models.FloatField(default=0)

    def __str__(self):
        return self.name

class History(models.Model):
    table_name = models.CharField(max_length=255)
    record_id = models.IntegerField()
    field_name = models.CharField(max_length=255)
    old_value = models.TextField()
    new_value = models.TextField()
    updated_at = models.DateTimeField()
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    message = models.TextField(null=True, blank=True)