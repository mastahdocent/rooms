"""warsztat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from rooms.views import (
    RoomListView, RoomDetailView, RoomEditView, RoomAddView, RoomDeleteView, ReservationAddView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RoomListView.as_view(), name="homepage"),
    path('room/<int:id>/', RoomDetailView.as_view(), name="room_detail"),
    path('room/modify/<int:id>/', RoomEditView.as_view(), name="room_modify"),
    path('room/new/', RoomAddView.as_view(), name="room_new"),
    path('room/delete/<int:id>/', RoomDeleteView.as_view(), name="room_delete"),
    path('room/reserve/<int:room_id>/', ReservationAddView.as_view(), name="reservation_add"),
]
