from django.db.models import Q
from django.contrib.auth import logout
from .models import Room, Device
from django.views import generic
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

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
        'is_logged_in': request.user.is_authenticated,
        'user': request.user,
    }
    return render(request, 'home.html', context)


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # Get the 'next' parameter from the URL
            next_url = request.GET.get('next')

            # If the 'next' parameter is present, redirect to that URL
            if next_url:
                return redirect(next_url)
            else:
                # Otherwise, redirect to the home page
                return redirect('home')    
    else:
        form = AuthenticationForm()

    context = {
        'form': form,
        'is_logged_in': request.user.is_authenticated,
        'user': request.user,
    }

    return render(request, 'login.html', context)

class DeviceListView(generic.ListView):
    model = Device
    context_object_name = 'device_list'   # your own name for the list as a template variable
    template_name = 'devices/device_list.html'  # Specify your own template name/location
    paginate_by = 5
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_logged_in'] = self.request.user.is_authenticated
        context['user'] = self.request.user
        return context

class DeviceDetailView(DetailView):
    model = Device
    context_object_name = 'device'
    template_name = 'devices/device_detail.html'
    paginate_by = 2
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_logged_in'] = self.request.user.is_authenticated
        context['user'] = self.request.user
        return context

class RoomListView(ListView):
    model = Room
    context_object_name = 'room_list'
    template_name = 'rooms/room_list.html'
    paginate_by = 5
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_logged_in'] = self.request.user.is_authenticated
        context['user'] = self.request.user
        return context

class RoomDetailView(DetailView):
    model = Room
    context_object_name = 'room'
    template_name = 'rooms/room_detail.html'
    paginate_by = 2
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_logged_in'] = self.request.user.is_authenticated
        context['user'] = self.request.user
        return context

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

class GuestView(TemplateView):
    template_name = 'guest.html'

    def get(self, request, *args, **kwargs):
        try:
            # Create a new guest user if it doesn't exist
            user = User.objects.get(username='guest')
        except User.DoesNotExist:
            # Create a new guest user
            user = User.objects.create_user(username='guest', password='guest1234')

        # Log the guest user in
        login(request, user)

        # Get the context data and pass it to the template
        context = self.get_context_data(**kwargs)
        context['is_logged_in'] = request.user.is_authenticated
        context['user'] = request.user
        return self.render_to_response(context)

def logout_view(request):
    logout(request)
    return redirect('login')  # Replace 'login_url' with the name of your login URL