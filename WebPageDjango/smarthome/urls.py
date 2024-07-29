from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('devices/', views.DeviceListView.as_view(), name='devices'),
    path('devices/<int:pk>/', views.DeviceDetailView.as_view(), name='device-detail'),
    # path('rooms/', views.RoomListView.as_view(), name='rooms'),
    # path('rooms/<int:pk>/', views.DeviceDetailView.as_view(), name='room-detail'),
]