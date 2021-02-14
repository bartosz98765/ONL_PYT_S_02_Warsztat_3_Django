"""reservation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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

from reservation_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.index, name='index'),
    path('room/new/', views.RoomNew.as_view(), name='new_room'),
    path('rooms', views.RoomsList.as_view(), name='rooms_list'),
    path('room/delete/<int:id>', views.RoomDelete.as_view(), name='room_delete'),
    path('room/modify/<int:id>', views.RoomModify.as_view(), name='room_modify'),
    path('room/reserve/<int:id>', views.Reservation.as_view(), name='room_reserve'),
    path('room/<int:id>', views.RoomDetails.as_view(), name='room_details'),
]
