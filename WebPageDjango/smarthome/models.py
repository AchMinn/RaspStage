from django.db import models
from django.utils.timezone import now
from django.core.exceptions import ValidationError
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
    last_connected = models.DateTimeField(default=timezone.now)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, related_name='devices')
    is_active = models.BooleanField(default=False)
    device_type = models.CharField(max_length=255, choices=[
        ('lampe', 'Lampe'), ('plug', 'Plug'), ('clima', 'Clima')
    ], default='lampe')
    intensity = models.IntegerField(null=True, blank=True, default=0)
    temperature = models.FloatField(null=True, blank=True, default=0)

    def clean(self):
        if self.intensity is not None and (self.intensity < 0 or self.intensity > 100):
            raise ValidationError('Intensity must be between 0 and 100.')
        if self.temperature is not None and self.temperature < 0:
            raise ValidationError('Temperature cannot be negative.')

    def save(self, *args, **kwargs):
        if self.pk is None:  # Only create outlets for new devices
            super().save(*args, **kwargs)  # Save the device first to get its ID
            if self.device_type == 'plug':
                for i in range(1, 5):  # Create 4 outlets
                    Outlet.objects.create(device=self, outlet_number=i)
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Outlet(models.Model):
    device = models.ForeignKey(Device, related_name='outlets', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    outlet_number = models.PositiveIntegerField()

    class Meta:
        unique_together = ('device', 'outlet_number')

    def clean(self):
        if self.outlet_number < 1:
            raise ValidationError('Outlet number must be a positive integer.')

    def __str__(self):
        return f"Outlet {self.outlet_number} on {self.device.name}"

class Measurement(models.Model):
    name = models.CharField(max_length=100)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    last_updated = models.DateTimeField(auto_now=True)
    value = models.FloatField(default=0)

    def clean(self):
        if self.value < 0:
            raise ValidationError('Measurement value cannot be negative.')

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