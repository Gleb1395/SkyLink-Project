from django.db import models
from django.db.models import F, Count


class FlightQuerySet(models.QuerySet):
    def with_available_seats(self):
        return self.annotate(
            available_seats=F("airplane__seat") + Count("flight_seats__ticket_flight")
        )


class FlightManager(models.Manager):

    def get_queryset(self):
        return FlightQuerySet(self.model, using=self._db)

    def with_available_seats(self):
        return self.get_queryset().with_available_seats()
