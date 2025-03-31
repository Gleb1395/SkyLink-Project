import random

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext as _

from airport.manager import FlightManager


class Flight(models.Model):
    """
    Associates a route, airplane, and crew with a specific flight.
    Stores information about departure and arrival times, flight status.
    Contains checks for correct time and calculates flight duration.
    """

    class Status(models.IntegerChoices):
        SCHEDULED = 1
        EN_ROUTE = 2
        DELAYED = 3
        CANCELLED = 4

    route = models.ForeignKey("Route", on_delete=models.CASCADE, related_name="flight_route")
    airplane = models.ForeignKey("Airplane", on_delete=models.CASCADE, related_name="flight_airplane")
    crew = models.ManyToManyField(
        "Crew",
        related_name="flight_crew",
    )
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    status = models.SmallIntegerField(choices=Status.choices, default=Status.SCHEDULED)
    objects = FlightManager()

    class Meta:
        verbose_name = _("Flight")
        verbose_name_plural = _("Flights")

    def __str__(self):
        return f"ID Flight:{self.id} "

    def clean(self):
        super().clean()
        if self.departure_time > self.arrival_time:
            raise ValidationError(_("Departure time must be earlier than Arrival time"))

    @property
    def duration(self):
        """
        Travel time calculation
        """
        return self.arrival_time - self.departure_time

    @property
    def formatted_duration(self):
        """
        Date Formatting
        """
        duration = self.duration
        hours, remainder = divmod(duration.total_seconds(), 3600)
        minutes, _ = divmod(remainder, 60)
        return f"{int(hours)}:{int(minutes)}"


class Route(models.Model):
    """
    Flight Route Model.

    Defines a route between two airports with distance and unique route code.
    """

    source = models.ForeignKey("Airport", on_delete=models.CASCADE, related_name="route_source")
    destination = models.ForeignKey("Airport", on_delete=models.CASCADE, related_name="route_destination")
    distance = models.IntegerField()
    code_route = models.CharField(max_length=10, unique=True)

    class Meta:
        verbose_name = _("Route")
        verbose_name_plural = _("Routes")
        constraints = [
            models.UniqueConstraint(
                fields=["source", "destination", "code_route"],
                name="unique_route_source",
            )
        ]

    def __str__(self):
        return f"{self.id} {self.code_route}"


class Airport(models.Model):
    """
    Airport Model.

    Contains information about the name, nearest major city, unique airport code and geographic coordinates.
    """

    name = models.CharField(max_length=120)
    closest_big_city = models.CharField(max_length=120)
    airport_code = models.CharField(max_length=20, unique=True)
    geographical_coordinates = models.FloatField()

    class Meta:
        verbose_name = _("Airport")
        verbose_name_plural = _("Airports")

    def __str__(self):
        return f"{self.name}"


class Airplane(models.Model):
    """
    Airplane model.

    Contains information about the aircraft name and type.
    """

    name = models.CharField(max_length=120)
    airplane_type = models.ForeignKey("AirplaneType", on_delete=models.CASCADE, related_name="airplane")

    class Meta:
        verbose_name = _("Airplane")
        verbose_name_plural = _("Airplanes")

    def __str__(self):
        return f"{self.name}"


class Seat(models.Model):
    """
    An airplane seat model.

    Describes a specific seat with number, row, seat type and class of service.
    Linked to the airplane and ticket class.
    """

    airplane = models.ForeignKey("Airplane", on_delete=models.CASCADE, related_name="seats_airplane")
    seat = models.SmallIntegerField(
        validators=[MinValueValidator(1)],
    )
    row = models.CharField(max_length=1)
    seat_type = models.CharField(
        max_length=50,
    )
    ticket_class = models.ForeignKey("TicketClass", on_delete=models.CASCADE, related_name="seat")

    class Meta:
        verbose_name = _("Seats")
        verbose_name_plural = _("Seats")
        unique_together = ("airplane", "seat", "row")

    def __str__(self):
        return f"ID {self.id}"


class FlightSeat(models.Model):
    """
    Flight Seat Reservation Model.

    Associates a specific seat with a specific flight.
    Checks if the airplane matches the flight and seat.
    """

    seat = models.ForeignKey("Seat", on_delete=models.CASCADE, related_name="flight_seats")
    flight = models.ForeignKey("Flight", on_delete=models.CASCADE, related_name="flight_seats")

    def clean(self):
        if self.seat.airplane != self.flight.airplane:
            raise ValidationError(_("Seat seat must belong to flight seat"))

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ("seat", "flight")
        verbose_name = _("Flight Seat")
        verbose_name_plural = _("Flight Seats")


class AirplaneType(models.Model):
    """
    Airplane type model.

    Stores the unique name of the aircraft type.
    """

    name = models.CharField(max_length=120, unique=True)

    class Meta:
        verbose_name = _("Airplane Type")
        verbose_name_plural = _("Airplane Types")

    def __str__(self):
        return f"{self.name}"


class Crew(models.Model):
    """
    Crew member model.

    Contains the first and last name of the crew member.
    """

    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)

    class Meta:
        verbose_name = _("Crew")
        verbose_name_plural = _("Crews")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Ticket(models.Model):
    """
    Ticket Model.

    Associates the ticket with the seat on the flight and the order, contains the ticket price.
    """

    flight_seat = models.ForeignKey("FlightSeat", on_delete=models.CASCADE, related_name="ticket_flight")
    order = models.ForeignKey("Order", on_delete=models.CASCADE, related_name="ticket_order")
    price = models.FloatField(validators=[MinValueValidator(0.0)])

    class Meta:
        verbose_name = _("Ticket")
        verbose_name_plural = _("Tickets")
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "flight_seat",
                ],
                name="unique_flight_seat_order",
            )
        ]

    def __str__(self):
        return f"{self.flight_seat} {self.order} {self.price}"


class TicketClass(models.Model):
    """
    Ticket class model.

    Defines the name and unique code of the class of service (e.g. Economy, Business).
    """

    name = models.CharField(
        max_length=120,
        unique=True,
    )

    class Meta:
        verbose_name = _("Ticket Class")
        verbose_name_plural = _("Ticket Classes")

    def __str__(self):
        return f"{self.name}"


class Tariff(models.Model):
    """
    Fare Model.

    Associates a fare with a ticket class and contains its code and name.
    """

    code = models.CharField(max_length=2, unique=True)
    name = models.CharField(max_length=100)
    ticket_class = models.ForeignKey("TicketClass", on_delete=models.CASCADE, related_name="tariff")

    class Meta:
        verbose_name = _("Tariff")
        verbose_name_plural = _("Tariffs")

    def __str__(self):
        return f"Tariff code: {self.code}, Tariff name: {self.name}, Ticket class: {self.ticket_class}"


class Order(models.Model):
    """
    Order Model.

    Contains information about the user and the time of order creation.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def __str__(self):
        return f"Order date: {self.created_at}"
