from django.db import models
from django.db.models import Count, F


class FlightQuerySet(models.QuerySet):
    def with_available_seats(self):
        return self.annotate(
            total_seats=Count("airplane__seats_airplane", distinct=True),
            booked_seats=Count("flight_seats__ticket_flight", distinct=True),
        ).annotate(available_seats=F("total_seats") - F("booked_seats"))


class FlightManager(models.Manager):

    def get_queryset(self):
        return FlightQuerySet(self.model, using=self._db)

    def with_available_seats(self):
        return self.get_queryset().with_available_seats()
