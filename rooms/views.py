import datetime

from django.db.models import Count, Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from django.urls import reverse

from rooms.models import Room, Reservation


class RoomListView(View):
    def get(self, request):
        today = datetime.date.today()
        rooms = Room.objects.all().annotate(
            reservations_count=Count(
                "reservations",
                filter=Q(reservations__date=today)
            )
        )

        return render(request, "homepage.html", context={
            "rooms": rooms,
            "selected_date": today
        })

    def post(self, request):
        selected_date = request.POST.get("date")
        rooms = Room.objects.all().annotate(
            reservations_count=Count(
                "reservations",
                filter=Q(reservations__date=selected_date)
            )
        )

        return render(request, "homepage.html", context={
            "rooms": rooms,
            "selected_date": datetime.datetime.strptime(selected_date, "%Y-%m-%d")
        })

class RoomDetailView(View):
    def get(self, request, id):
        # try:
        #     room = Room.objects.get(id=id)
        # except Room.DoesNotExist:
        #     raise Http404

        today = datetime.date.today()
        room = get_object_or_404(Room, id=id)
        reservations = Reservation.objects.filter(room=room, date__gte=today)

        return render(request, "room_detail.html", context={
            "room": room,
            "reservations": reservations,
        })


class RoomEditView(View):
    def get(self, request, id):
        room = get_object_or_404(Room, id=id)
        return render(request, "room_edit.html", context={
            "room": room
        })

    def post(self, request, id):
        room = get_object_or_404(Room, id=id)

        room.name = request.POST.get("name")
        room.capacity = int(request.POST.get("capacity"))
        room.projector = request.POST.get("projector") == "on"

        room.save()
        return redirect(reverse("room_detail", kwargs={"id": room.id}))


class RoomAddView(View):
    def get(self, request):
        return render(request, "room_edit.html")

    def post(self, request):
        room = Room()

        room.name = request.POST.get("name")
        room.capacity = int(request.POST.get("capacity"))
        room.projector = request.POST.get("projector") == "on"

        room.save()
        return redirect(reverse("room_detail", kwargs={"id": room.id}))


class RoomDeleteView(View):
    def get(self, request, id):
        room = get_object_or_404(Room, id=id)
        return render(request, "room_delete.html", context={
            "room": room
        })

    def post(self, request, id):
        room = get_object_or_404(Room, id=id)
        room.delete()
        return redirect(reverse("homepage"))


class ReservationAddView(View):
    def get(self, request, room_id):
        room = get_object_or_404(Room, id=room_id)
        return render(request, "reservation_edit.html", context={
            "room": room
        })

    def post(self, request, room_id):
        date = request.POST.get("date")
        comment = request.POST.get("comment")
        Reservation.objects.create(date=date, comment=comment, room_id=room_id)
        return redirect(reverse("room_detail", kwargs={"id": room_id}))
