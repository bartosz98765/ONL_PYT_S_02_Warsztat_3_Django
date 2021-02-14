from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from reservation_app.models import Rooms, Reservations
import datetime

def index(request):
    return render(request, 'base.html', {'title': 'Room reservation'})

class RoomNew(View):

    def get(self, request):
        context = {'title': 'Add new room'}
        return render(request, 'room-new.html', context)

    def post(self, request):
        # tu chyba można pobrać wszystko jednym request.POST i przypisać w jednej linii do zmiennych, sprawdzić to!!!
        room_name = request.POST.get('room_name')
        capacity = int(request.POST['capacity'])
        projector = True if request.POST.get('projector') == 'on' else False

        if room_name != '':
            if capacity > 0:
                try:
                    Rooms.objects.create(name=room_name, capacity=capacity, is_projector=projector)
                except Exception as err:
                    error = err
                    return render(request, 'room-new.html', {'title': "Add new room", 'error': error})
            else:
                error = "Wrong capacity value!"
                return render(request, 'room-new.html', {'title': "Add new room", 'error': error})
        else:
            error = "Name cannot be empty!"
            return render(request, 'room-new.html', {'title': "Add new room", 'error': error})

        return redirect('rooms_list')


class RoomsList(View):

    def get(self, request):
        rooms = Rooms.objects.all()
        reservations = Reservations.objects.filter(date='2021-02-14')

        today_iso = datetime.date.today().isoformat()

        context = {'rooms': rooms,
                   'today_iso': today_iso,
                   'reservations': reservations,
                   'title': 'Room reservation'}

        return render(request, 'rooms.html', context)

    # def post(self, request, id):
    #     submit = request.POST['submit']
        # if submit == 'edit':
        #     return request('room_edit')
        # if submit == 'delete':
        #     return render(request, 'room/delete/')
        # if submit == 'reserve':
        #     return request('room_reserve')


class RoomDelete(View):

    def get(self, request, id):
        room = Rooms.objects.get(pk=id)
        context = {'room': room}
        return render(request, 'room-delete.html', context)

    def post(self, request, id):
        if request.POST['delete'] == 'YES':
            room = Rooms.objects.get(pk=id)
            room.delete()
        return redirect('rooms_list')


class RoomModify(View):

    def get(self, request, id):
        room = Rooms.objects.get(pk=id)
        context = {'room': room}
        return render(request, 'room-modify.html', context)

    def post(self, request, id):
        # tu chyba można pobrać wszystko jednym request.POST i przypisać w jednej linii do zmiennych, sprawdzić to!!!
        # trzeba dodać pole hidden albo session, albo ciasteczka by przekazać ID
        room_name = request.POST.get('room_name')
        room_id = request.POST.get('room_id')
        capacity = int(request.POST['capacity'])
        projector = True if request.POST.get('projector') == 'on' else False

        if room_name != '':
            if capacity > 0:
                try:
                    room = Rooms.objects.get(pk=room_id)
                    room.name = room_name
                    room.capacity = capacity
                    room.is_projector = projector
                    room.save()
                except Exception as e:
                    error = e
                    room = Rooms.objects.get(pk=room_id)
                    context = {'error': error, 'room': room, 'title': 'Modify room'}
                    return render(request, 'room-modify.html', context)
            else:
                error = "Wrong capacity value!"
                room = Rooms.objects.get(pk=room_id)
                context = {'error': error, 'room': room, 'title':'Modify room'}
                return render(request, 'room-modify.html', context)
        else:
            error = "Name cannot be empty!"
            room = Rooms.objects.get(pk=room_id)
            context = {'error': error, 'room': room, 'title': 'Modify room'}
            return render(request, 'room-modify.html', context)

        return redirect('rooms_list')


class Reservation(View):
    
    def get(self, request, id):
        room = Rooms.objects.get(pk=id)
        reserved_days = room.room_reservation.all().order_by('-date')
        context = {'room': room, 'reserved_days':reserved_days, 'title': 'Room reservation'}
        return render(request, 'room-reserve.html', context)

    def post(self, request, id):
        date = request.POST['date']
        comment = request.POST['comment']
        room = Rooms.objects.get(pk=id)
        if date >= datetime.date.today().isoformat():
            try:
                Reservations.objects.create(date=date, room=room, comment=comment)
            except Exception as e:
                error = e
                context = {'error': error, 'title': 'Room reservation'}
                return render(request, 'room-reserve.html', context)
        else:
            error = "Error: date in the past"
            room = Rooms.objects.get(pk=id)
            context = {'error':error, 'room': room, 'title': 'Room reservation'}
            return render(request, 'room-reserve.html', context)
        return redirect('rooms_list')

class RoomDetails(View):

    def get(self, request, id):
        room = Rooms.objects.get(pk=id)
        today_iso = datetime.date.today().isoformat()
        reserved_days = room.room_reservation.filter(date__gte = today_iso).order_by('-date')
        context = {'room': room, 'reserved_days': reserved_days, 'title': 'Room details'}
        return render(request, 'room-details.html', context)