from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=128)
    capacity = models.SmallIntegerField()
    projector = models.BooleanField()

    def __str__(self):
        return self.name


class Reservation(models.Model):
    date = models.DateField()
    comment = models.TextField(null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="reservations")

    def __str__(self):
        return f"{self.room} na {self.date}"
