from django.contrib import admin
from .models import Room, Device, Sensor, Measurement, User
from django.contrib.auth.admin import UserAdmin

class DeviceInline(admin.TabularInline):
    model = Device
    extra = 0

class SensorInline(admin.TabularInline):
    model = Sensor
    extra = 0

class MeasurementInline(admin.TabularInline):
    model = Measurement
    extra = 0

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    inlines = [DeviceInline]

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'room', 'is_active')
    list_filter = ('room', 'is_active')
    search_fields = ('name', 'description')
    inlines = [SensorInline, MeasurementInline]

@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'device', 'value', 'last_updated')
    list_filter = ('device',)
    search_fields = ('name', 'description')

@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_updated', 'device', 'value')
    list_filter = ('device',)
    search_fields = ('name', 'value')
