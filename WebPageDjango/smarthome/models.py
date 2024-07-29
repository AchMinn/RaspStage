from django.db import models

class Room(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class Device(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, related_name='devices')
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('device_detail', kwargs={'pk': self.pk})

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