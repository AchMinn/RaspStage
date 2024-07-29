from django.db import models
from django.utils.timezone import now

class Room(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    @property

    def device_count(self):
        return self.devices.count()

    def save(self, *args, **kwargs):
        # Update the updated_at field whenever the model is saved
        self.updated_at = now()
        super().save(*args, **kwargs)

class Device(models.Model):
    name = models.CharField(max_length=100)
    model = models.CharField(max_length=100, default='Unknown')
    description = models.TextField(null=True, blank=True)
    processor = models.CharField(max_length=100, null=True, blank=True)
    ram = models.CharField(max_length=100, null=True, blank=True)
    storage = models.CharField(max_length=100, null=True, blank=True)
    display = models.CharField(max_length=100, null=True, blank=True)
    connectivity = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='device_images', null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, related_name='devices')
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Sensor(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='sensors')
    value = models.FloatField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Setting(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='settings')
    value = models.CharField(max_length=100)

    def __str__(self):
        return self.name