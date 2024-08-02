from django.urls import path
from django.shortcuts import redirect
from . import views
from .views import CustomLogoutView


urlpatterns = [
    path('', views.login_view, name='login'),
    path('home/', views.home_view, name='home'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('guest/', views.GuestView.as_view(), name='guest'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('devices/', views.DeviceListView.as_view(), name='devices'),
    path('devices/<int:pk>/', views.DeviceDetailView.as_view(), name='device-detail'),
    path('rooms/', views.RoomListView.as_view(), name='rooms'),
    path('rooms/<int:pk>/', views.RoomDetailView.as_view(), name='room-detail'),
]