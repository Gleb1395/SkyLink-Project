import random

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext as _

from airport.manager import FlightManager


class Flight(models.Model):  # TODO make testcase
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
        return f"{self.route} {self.airplane} {self.departure_time} {self.arrival_time}"

    def clean(self):
        super().clean()
        if self.departure_time > self.arrival_time:
            raise ValidationError(_("Departure time must be earlier than Arrival time"))


class Route(models.Model):  # TODO make testcase
    source = models.ForeignKey("Airport", on_delete=models.CASCADE, related_name="route_source")
    destination = models.ForeignKey("Airport", on_delete=models.CASCADE, related_name="route_destination")
    distance = models.IntegerField()
    code_route = models.CharField(max_length=10, unique=True)

    class Meta:
        verbose_name = _("Route")
        verbose_name_plural = _("Routes")
        unique_together = ("source", "destination")

    def __str__(self):
        return f"{self.source} {self.distance} {self.destination}"


class Airport(models.Model):
    name = models.CharField(max_length=120)
    closest_big_city = models.CharField(max_length=120)
    airport_code = models.CharField(max_length=20, unique=True)
    geographical_coordinates = models.FloatField()  # TODO ditch the validator

    class Meta:
        verbose_name = _("Airport")
        verbose_name_plural = _("Airports")

    def __str__(self):
        return f"{self.name} {self.closest_big_city}"


class Airplane(models.Model):
    name = models.CharField(max_length=120)
    airplane_type = models.ForeignKey("AirplaneType", on_delete=models.CASCADE, related_name="airplane")

    class Meta:
        verbose_name = _("Airplane")
        verbose_name_plural = _("Airplanes")

    def __str__(self):
        return f"{self.name} {self.airplane_type}"


class Seat(models.Model):  # TODO make testcase
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
        return f"Seat: {self.seat},  Row: {self.row}, Type seat: {self.seat_type}, Class: {self.ticket_class}"


class FlightSeat(models.Model):
    seat = models.ForeignKey("Seat", on_delete=models.CASCADE, related_name="flight_seats")
    flight = models.ForeignKey("Flight", on_delete=models.CASCADE, related_name="flight_seats")

    class Meta:
        unique_together = ("seat", "flight")
        verbose_name = _("Flight Seat")
        verbose_name_plural = _("Flight Seats")

    def __str__(self):
        return f"{self.seat} {self.flight}"


class AirplaneType(models.Model):
    name = models.CharField(max_length=120, unique=True)

    class Meta:
        verbose_name = _("Airplane Type")
        verbose_name_plural = _("Airplane Types")

    def __str__(self):
        return f"{self.name}"


class Crew(models.Model):
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)

    class Meta:
        verbose_name = _("Crew")
        verbose_name_plural = _("Crews")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Ticket(models.Model):
    flight_seat = models.ForeignKey("FlightSeat", on_delete=models.CASCADE, related_name="ticket_flight")
    order = models.ForeignKey("Order", on_delete=models.CASCADE, related_name="ticket_order")
    price = models.FloatField(validators=[MinValueValidator(0.0)])  # TODO make testcase

    class Meta:
        verbose_name = _("Ticket")
        verbose_name_plural = _("Tickets")
        unique_together = ("flight_seat", "order")

    def __str__(self):
        return f"{self.flight_seat} {self.order} {self.price}"


class TicketClass(models.Model):  # TODO make testcase
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
    code = models.CharField(max_length=2, unique=True)
    name = models.CharField(max_length=100)
    ticket_class = models.ForeignKey("TicketClass", on_delete=models.CASCADE, related_name="tariff")

    class Meta:
        verbose_name = _("Tariff")
        verbose_name_plural = _("Tariffs")

    def __str__(self):
        return f"Tariff code: {self.code}, Tariff name: {self.name}, Ticket class: {self.ticket_class}"


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def __str__(self):
        return f"Order date: {self.created_at}, User:{self.user}"
