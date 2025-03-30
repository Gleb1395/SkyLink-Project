from django.db import models
from django.db.models import Count, F


class FlightQuerySet(models.QuerySet):
    """
    QuerySet for Flight model.

    Adds an annotation with the number of available seats on flights:
    - total_seats: total number of seats.
    - booked_seats: number of seats already booked.
    - available_seats: the number of available seats.
    """

    def with_available_seats(self):
        return self.annotate(
            total_seats=Count("airplane__seats_airplane", distinct=True),
            booked_seats=Count("flight_seats__ticket_flight", distinct=True),
        ).annotate(available_seats=F("total_seats") - F("booked_seats"))


class FlightManager(models.Manager):
    """
    Manager for the Flight model.

    Extends the base queryset with a method:
    - with_available_seats(): returns flights annotated with available seats.
    """

    def get_queryset(self):
        return FlightQuerySet(self.model, using=self._db)

    def with_available_seats(self):
        return self.get_queryset().with_available_seats()
