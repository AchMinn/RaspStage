from django.db import models
from django.utils.timezone import now
from django.utils import timezone
from django.contrib.auth.models import User

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
        return self.device_set.count()

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            History.objects.create(
                table_name='Room',
                record_id=self.pk,
                field_name='all',
                old_value='',
                new_value=str(self),
                updated_at=now(),
                updated_by=kwargs.get('user', None),
                message='New room created'
            )
        else:
            History.objects.create(
                table_name='Room',
                record_id=self.pk,
                field_name='all',
                old_value=str(self),
                new_value=str(self),
                updated_at=now(),
                updated_by=kwargs.get('user', None),
                message='Room updated'
            )

    def delete(self, *args, **kwargs):
        History.objects.create(
            table_name='Room',
            record_id=self.pk,
            field_name='all',
            old_value=str(self),
            new_value='',
            updated_at=now(),
            updated_by=kwargs.get('user', None),
            message='Room deleted'
        )
        super().delete(*args, **kwargs)

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
    ],default="Sensor")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            History.objects.create(
                table_name='Device',
                record_id=self.pk,
                field_name='all',
                old_value='',
                new_value=str(self),
                updated_at=now(),
                updated_by=kwargs.get('user', None),
                message='New device created'
            )
        else:
            History.objects.create(
                table_name='Device',
                record_id=self.pk,
                field_name='all',
                old_value=str(self),
                new_value=str(self),
                updated_at=now(),
                updated_by=kwargs.get('user', None),
                message='Device updated'
            )

    def delete(self, *args, **kwargs):
        History.objects.create(
            table_name='Device',
            record_id=self.pk,
            field_name='all',
            old_value=str(self),
            new_value='',
            updated_at=now(),
            updated_by=kwargs.get('user', None),
            message='Device deleted'
        )
        super().delete(*args, **kwargs)

class Sensor(models.Model):
    name = models.CharField(max_length=100)
    sensor_type = models.CharField(max_length=255, default="NAN")
    description = models.TextField(null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, related_name='devices')
    value = models.FloatField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            History.objects.create(
                table_name='Sensor',
                record_id=self.pk,
                field_name='all',
                old_value='',
                new_value=str(self),
                updated_at=now(),
                updated_by=kwargs.get('user', None),
                message='New sensor created'
            )
        else:
            History.objects.create(
                table_name='Sensor',
                record_id=self.pk,
                field_name='all',
                old_value=str(self),
                new_value=str(self),
                updated_at=now(),
                updated_by=kwargs.get('user', None),
                message='Sensor updated'
            )

    def delete(self, *args, **kwargs):
        History.objects.create(
            table_name='Sensor',
            record_id=self.pk,
            field_name='all',
            old_value=str(self),
            new_value='',
            updated_at=now(),
            updated_by=kwargs.get('user', None),
            message='Sensor deleted'
        )
        super().delete(*args, **kwargs)

class Measurement(models.Model):
    name = models.CharField(max_length=100)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    last_updated = models.DateTimeField(auto_now=True)
    value = models.FloatField(default=0)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            History.objects.create(
                table_name='Measurement',
                record_id=self.pk,
                field_name='all',
                old_value='',
                new_value=str(self),
                updated_at=now(),
                updated_by=kwargs.get('user', None),
                message='New measurement created'
            )
        else:
            History.objects.create(
                table_name='Measurement',
                record_id=self.pk,
                field_name='all',
                old_value=str(self),
                new_value=str(self),
                updated_at=now(),
                updated_by=kwargs.get('user', None),
                message='Measurement updated'
            )

    def delete(self, *args, **kwargs):
        History.objects.create(
            table_name='Measurement',
            record_id=self.pk,
            field_name='all',
            old_value=str(self),
            new_value='',
            updated_at=now(),
            updated_by=kwargs.get('user', None),
            message='Measurement deleted'
        )
        super().delete(*args, **kwargs)

class History(models.Model):
    table_name = models.CharField(max_length=255)
    record_id = models.IntegerField()
    field_name = models.CharField(max_length=255)
    old_value = models.TextField()
    new_value = models.TextField()
    updated_at = models.DateTimeField()
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(null=True, blank=True)