from django.http import HttpResponseRedirect
from .models import Room, Device, History, Measurement
from django.conf import settings
from django.utils import timezone
from django.db.models import Q, Sum
from django.contrib.auth import logout
from django.views import generic
from django.views.generic import ListView, DetailView, CreateView, TemplateView, DeleteView, UpdateView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, models
from django.utils.dateparse import parse_date


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
        
        action = request.POST.get('action')
        intensity = request.POST.get('intensity')

        # Prepare common fields for the History log
        table_name = 'Device'  # Change this if needed
        updated_at = timezone.now()
        updated_by = request.user  # Assuming the user is logged in
        message = None

        # Control logic based on the action
        if action == 'turn_on':
            if not self.object.is_active:  # Log change only if the state is changing
                self.object.is_active = True
                self.object.save()
                message = "Device turned on"
                History.objects.create(
                    table_name=table_name,
                    record_id=self.object.id,
                    field_name='is_active',
                    old_value='False',
                    new_value='True',
                    updated_at=updated_at,
                    updated_by=updated_by,
                    message=message
                )

        elif action == 'turn_off':
            if self.object.is_active:  # Log change only if the state is changing
                self.object.is_active = False
                self.object.save()
                message = "Device turned off"
                History.objects.create(
                    table_name=table_name,
                    record_id=self.object.id,
                    field_name='is_active',
                    old_value='True',
                    new_value='False',
                    updated_at=updated_at,
                    updated_by=updated_by,
                    message=message
                )

        elif action == 'change_intensity' and intensity is not None:
            # Assuming you want to log intensity changes
            old_value = str(self.object.intensity) if hasattr(self.object, 'intensity') else 'N/A'
            self.object.intensity = float(intensity)  # Assuming you have an intensity field
            self.object.save()
            History.objects.create(
                table_name=table_name,
                record_id=self.object.id,
                field_name='intensity',
                old_value=old_value,
                new_value=intensity,
                updated_at=updated_at,
                updated_by=updated_by,
                message="Intensity changed"
            )
        
        # Redirect back to the control page
        return redirect('device-control', pk=self.object.id)

class DeviceCreateView(CreateView):
    model = Device
    template_name = 'devices/device_create.html'
    fields = ['name', 'model', 'description', 'room', 'is_active', 'device_type']
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
    fields = ['name', 'model', 'description', 'room', 'device_type']
    success_url = reverse_lazy('devices')

    def form_valid(self, form):
        # Get the original device instance
        original_device = self.get_object()
        
        # Set the updated_by field
        form.instance.updated_by = self.request.user

        # Save the updated device
        response = super().form_valid(form)

        # Create History records for changed fields
        changed_fields = []
        for field in form.changed_data:
            old_value = getattr(original_device, field)
            new_value = getattr(form.instance, field)
            if old_value != new_value:
                changed_fields.append((field, old_value, new_value))

                # Create individual History record for each changed field
                History.objects.create(
                    table_name='devices',
                    record_id=form.instance.id,
                    field_name=field,
                    old_value=str(old_value),
                    new_value=str(new_value),
                    updated_at=timezone.now(),
                    updated_by=self.request.user,
                    message=f'Device "{original_device.name}" was updated. Changes: {changed_fields}"'
                )

        # Optional: You can log a summary message if needed
        if changed_fields:
            summary_message = f'Device "{original_device.name}" was updated. Changes: {changed_fields}'
            # Log or handle summary_message as necessary

        return response

        return response
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_logged_in'] = self.request.user.is_authenticated
        context['user'] = self.request.user
        return context

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_logged_in'] = self.request.user.is_authenticated
        context['user'] = self.request.user
        context['device_count'] = self.object.device_count
        context['devices'] = self.object.devices.all()  # Fetch all devices for the room
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
    return redirect('login')  


class HistoryDashboardView(LoginRequiredMixin, ListView):
    model = History
    template_name = 'logs/history/history_dashboard.html'
    context_object_name = 'history_records'
    ordering = ['-updated_at']
    paginate_by = 10

    def get_queryset(self):
        queryset = History.objects.all().order_by('-updated_at')  # Ensure proper ordering
        
        table_name = self.request.GET.get('table_name')
        record_id = self.request.GET.get('record_id')
        field_name = self.request.GET.get('field_name')
        updated_at = self.request.GET.get('updated_at')


        if table_name:
            queryset = queryset.filter(table_name__icontains=table_name)
        if record_id:
            queryset = queryset.filter(record_id=record_id)
        if field_name:
            queryset = queryset.filter(field_name__icontains=field_name)
        if updated_at:
            queryset = queryset.filter(updated_at__date=updated_at)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_name'] = self.request.GET.get('table_name', '')
        context['record_id'] = self.request.GET.get('record_id', '')
        context['field_name'] = self.request.GET.get('field_name', '')
        context['updated_at'] = self.request.GET.get('updated_at', '')  
        context['is_logged_in'] = self.request.user.is_authenticated
        context['user'] = self.request.user
        return context

class ConsumptionDashboardView(LoginRequiredMixin, ListView):
    model = Measurement
    template_name = 'logs/consumption/consumption_dashboard.html'
    context_object_name = 'consumption_records'
    ordering = ['-last_updated']
    paginate_by = 10

    def get_queryset(self):
        queryset = Measurement.objects.all()
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')

        if start_date:
            start_date = parse_date(start_date)
            if start_date:
                queryset = queryset.filter(last_updated__gte=start_date)
                
        if end_date:
            end_date = parse_date(end_date)
            if end_date:
                queryset = queryset.filter(last_updated__lte=end_date)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        start_date = self.request.GET.get('start_date', '')
        end_date = self.request.GET.get('end_date', '')

        context['start_date'] = start_date
        context['end_date'] = end_date
        context['devices'] = Device.objects.all()
        context['is_logged_in'] = self.request.user.is_authenticated
        context['user'] = self.request.user

        # Fetch consumption records
        consumption_records = self.get_queryset()
        context['consumption_records'] = consumption_records

        # Aggregate consumption by device type
        device_types = Device.objects.values_list('device_type', flat=True).distinct()
        consumption_by_device_type = {
            device_type: consumption_records.filter(device__device_type=device_type).aggregate(total=Sum('value'))['total'] or 0
            for device_type in device_types
        }

        context['device_types'] = list(device_types)
        context['consumption_by_device_type'] = [consumption_by_device_type.get(device_type, 0) for device_type in device_types]

        return context