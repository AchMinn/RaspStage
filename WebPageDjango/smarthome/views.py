from django.db.models import Q
from django.shortcuts import render
from .models import Room, Device
from django.views import generic
from django.views.generic import ListView, DetailView
from django.shortcuts import render

def home_view(request):
    """View function for the home page of the smart home application."""

    # Generate counts of some of the main objects
    num_rooms = Room.objects.all().count()
    num_devices = Device.objects.all().count()

    # Active devices (is_active = True)
    num_devices_active = Device.objects.filter(is_active=True).count()

    # Get a list of unique device names
    device_names = Device.objects.values_list('name', flat=True).distinct()
    num_device_types = len(device_names)

    # Generate counts for devices and rooms containing a particular word (case-insensitive)
    search_word = request.GET.get('search_word', '').lower()
    num_rooms_containing = Room.objects.filter(Q(name__icontains=search_word)).count()
    num_devices_containing = Device.objects.filter(Q(name__icontains=search_word)).count()

    context = {
        'num_rooms': num_rooms,
        'num_devices': num_devices,
        'num_devices_active': num_devices_active,
        'num_device_types': num_device_types,
        'num_rooms_containing': num_rooms_containing,
        'num_devices_containing': num_devices_containing,
        'search_word': search_word,
    }

    # Render the HTML template home.html with the data in the context variable
    return render(request, 'home.html', context=context)

class DeviceListView(generic.ListView):
    model = Device
    context_object_name = 'device_list'   # your own name for the list as a template variable
    template_name = 'devices/device_list.html'  # Specify your own template name/location
    paginate_by = 5

class DeviceDetailView(DetailView):
    model = Device
    context_object_name = 'device'
    template_name = 'devices/device_detail.html'
    paginate_by = 
2
class RoomListView(ListView):
    model = Room
    context_object_name = 'room_list'
    template_name = 'rooms/room_list.html'
    paginate_by = 5

class RoomDetailView(DetailView):
    model = Room
    context_object_name = 'room'
    template_name = 'rooms/room_detail.html'
    paginate_by = 2
