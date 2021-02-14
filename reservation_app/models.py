from django.db import models

class Rooms(models.Model):
    name = models.CharField(max_length=255, unique=True)
    capacity = models.PositiveIntegerField()
    is_projector = models.BooleanField(default=False)


class Reservations(models.Model):
    date = models.DateField()
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE, related_name='room_reservation')
    comment = models.CharField(max_length=128)
    class Meta:
        unique_together = ('date', 'room')
