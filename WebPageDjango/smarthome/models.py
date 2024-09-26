from django.utils import timezone
from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError

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
    DEVICE_TYPE_CHOICES = [
        ('lampe', 'Lampe'), 
        ('plug', 'Plug'), 
        ('clima', 'Clima')
    ]

    MODE_CHOICES = [
        ('auto', 'Auto'),
        ('cool', 'Cool'),
        ('dry', 'Dry'),
        ('heat', 'Heat'),
        ('fan', 'Fan'),
    ]

    FAN_SPEED_CHOICES = [
        ('auto', 'Auto'),
        ('min', 'Min'),
        ('med', 'Med'),
        ('max', 'Max'),
    ]

    name = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    last_connected = models.DateTimeField(default=timezone.now)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, related_name='devices')
    is_active = models.BooleanField(default=False)
    device_type = models.CharField(max_length=255, choices=DEVICE_TYPE_CHOICES, default='lampe')
    intensity = models.IntegerField(null=True, blank=True, default=0)
    temperature = models.FloatField(null=True, blank=True, default=0)
    
    # Additional fields for climate control
    mode = models.CharField(max_length=10, choices=MODE_CHOICES, default='auto')
    fan_speed = models.CharField(max_length=10, choices=FAN_SPEED_CHOICES, default='auto')
    turbo = models.BooleanField(default=False)
    swing = models.BooleanField(default=False)
    led = models.BooleanField(default=False)
    sleep = models.BooleanField(default=False)

    def clean(self):
        if self.intensity is not None and (self.intensity < 0 or self.intensity > 100):
            raise ValidationError('Intensity must be between 0 and 100.')
        if self.temperature is not None and self.temperature < 0:
            raise ValidationError('Temperature cannot be negative.')

        # Check limits for device types
        self.check_device_limits()

    def check_device_limits(self):
        limit = 0
        if self.device_type in ['lampe', 'plug']:
            limit = 5
        elif self.device_type == 'clima':
            limit = 3
        
        current_count = Device.objects.filter(device_type=self.device_type).count()
        if current_count >= limit and self.pk is None:  # Only check for new devices
            raise ValidationError(f"You can only have {limit} {self.device_type}s.")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

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

    def __str__(self):
        return f"History of {self.table_name} ID {self.record_id} at {self.updated_at}"