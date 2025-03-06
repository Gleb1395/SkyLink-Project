from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models


class Flight(models.Model):
    route = models.ForeignKey("Route", on_delete=models.CASCADE, related_name="flight_rote")
    airplane = models.ForeignKey("Airplane", on_delete=models.CASCADE, related_name="flight_airplane")
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()


class Route(models.Model):
    source = models.ForeignKey("Airport", on_delete=models.CASCADE, related_name="route_source")
    destination = models.ForeignKey("Airport", on_delete=models.CASCADE, related_name="route_destination")
    distance = models.IntegerField()


class Airport(models.Model):
    name = models.CharField(max_length=120)
    closest_big_city = models.CharField(max_length=120)


class Airplane(models.Model):
    name = models.CharField(max_length=120)
    rows = models.SmallIntegerField()
    seats_in_row = models.SmallIntegerField()
    airplane_type = models.ForeignKey("AirplaneType", on_delete=models.CASCADE, related_name="airplanes")


class AirplaneType(models.Model):
    name = models.CharField(max_length=120)


class Crew(models.Model):
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)


class Ticket(models.Model):
    row = models.SmallIntegerField()
    seat = models.SmallIntegerField()
    flight = models.ForeignKey("Flight", on_delete=models.CASCADE, related_name="ticket_flight")
    order = models.ForeignKey("Order", on_delete=models.CASCADE, related_name="ticket_order")


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
