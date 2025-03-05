import uuid

from django.contrib.auth.models import User
from django.db import models


class Flights(models.Model):
    route = ...
    airplane = ...
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()


class Route(models.Model):
    source = "Airport"
    destination = "Airport"
    distance = models.IntegerField()


class Airport(models.Model):
    name = models.CharField(max_length=120)
    closest_big_city = models.CharField(max_length=120)


class Airplane(models.Model):
    name = models.CharField(max_length=120)
    rows = models.SmallIntegerField()
    seats_in_row = models.SmallIntegerField()
    airplane_type = ...


class AirplaneType(models.Model):
    name = models.CharField(max_length=120)


class Crew(models.Model):
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)


class Ticket(models.Model):
    row = models.SmallIntegerField()
    seat = models.SmallIntegerField()
    flight = ...
    order = ...


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
