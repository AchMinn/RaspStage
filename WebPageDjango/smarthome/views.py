from .models import Room, Device, History
from django.conf import settings
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth import logout
from django.views import generic
from django.views.generic import ListView, DetailView, CreateView, TemplateView, DeleteView, UpdateView
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
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

class DeviceControlView(DetailView):
    model = Device
    context_object_name = 'device'
    template_name = 'devices/device_control.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_logged_in'] = self.request.user.is_authenticated
        context['user'] = self.request.user
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Add your device control logic here
        # For example, you can update the device's state based on the form data
        self.object.is_active = not self.object.is_active
        self.object.save()
        return self.render_to_response(self.get_context_data())

class DeviceCreateView(CreateView):
    model = Device
    template_name = 'devices/device_create.html'
    fields = ['name', 'model', 'description', 'manufacturer', 'firmware', 'room', 'is_active', 'device_type']
    success_url = reverse_lazy('devices')
    permission_required = 'devices.create_device'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_logged_in'] = self.request.user.is_authenticated
        context['user'] = self.request.user
        context['room_list'] = Room.objects.all()
        return context

    def form_valid(self, form):
            form.instance.created_by = self.request.user
            form.instance.updated_by = self.request.user
            response = super().form_valid(form)

            # Create the History record
            History.objects.create(
                table_name='devices',
                record_id=self.object.id,
                field_name='',
                old_value='',
                new_value=str(self.object),
                updated_at=timezone.now(),
                updated_by=self.request.user,
                message=f'Device "{self.object.name}" was created.'
            )

            return response

class DeviceUpdateView(UpdateView):
    model = Device
    template_name = 'devices/device_update.html'
    fields = ['name', 'model', 'description', 'manufacturer', 'firmware', 'room', 'device_type']
    success_url = reverse_lazy('devices')

class DeviceDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Device
    template_name = 'devices/device_confirm_delete.html'
    success_url = reverse_lazy('devices')
    permission_required = 'devices.delete_device'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_logged_in'] = self.request.user.is_authenticated
        context['user'] = self.request.user
        return context

    def delete(self, request, *args, **kwargs):
            self.object = self.get_object()
            success_url = self.get_success_url()

            # Create the History record
            History.objects.create(
                table_name='devices',
                record_id=self.object.id,
                field_name='',
                old_value='',
                new_value='',
                updated_at=timezone.now(),
                updated_by=request.user,
                message=f'Device "{self.object.name}" was deleted.'
            )

            self.object.delete()
            return HttpResponseRedirect(success_url)

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


class HistoryDashboardView(LoginRequiredMixin, ListView):
    model = History
    template_name = 'history/history_dashboard.html'
    context_object_name = 'history_records'
    ordering = ['-updated_at']

    def get_queryset(self):
        queryset = History.objects.all()
        table_name = self.request.GET.get('table_name')
        record_id = self.request.GET.get('record_id')
        field_name = self.request.GET.get('field_name')

        if table_name:
            queryset = queryset.filter(table_name__icontains=table_name)
        if record_id:
            queryset = queryset.filter(record_id=record_id)
        if field_name:
            queryset = queryset.filter(field_name__icontains=field_name)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_name'] = self.request.GET.get('table_name', '')
        context['record_id'] = self.request.GET.get('record_id', '')
        context['field_name'] = self.request.GET.get('field_name', '')
        context['is_logged_in'] = self.request.user.is_authenticated
        context['user'] = self.request.user
        return context