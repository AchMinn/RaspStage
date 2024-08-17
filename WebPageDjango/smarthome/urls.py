from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('home/', views.home_view, name='home'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('guest/', views.GuestView.as_view(), name='guest'),
    path('logout/', views.logout_view, name='logout'),
    path('devices/', views.DeviceListView.as_view(), name='devices'),
    path('devices/<int:pk>/', views.DeviceDetailView.as_view(), name='device-detail'),
    path('devices/<int:pk>/control/', views.DeviceControlView.as_view(), name='device-control'),
    path('devices/create/', views.DeviceCreateView.as_view(), name='device-create'),
    path('devices/<int:pk>/update/', views.DeviceUpdateView.as_view(), name='device-update'),
    path('devices/<int:pk>/delete/', views.DeviceDeleteView.as_view(), name='device-delete'),
    path('rooms/', views.RoomListView.as_view(), name='rooms'),
    path('rooms/<int:pk>/', views.RoomDetailView.as_view(), name='room-detail'),
    path('history/', views.HistoryDashboardView.as_view(), name='history-dashboard'),

]