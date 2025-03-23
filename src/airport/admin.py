from django.contrib import admin

from airport.models import (Airplane, AirplaneType, Airport, Crew, Flight,
                            FlightSeat, Order, Route, Seat, Tariff, Ticket,
                            TicketClass)


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = (
        "route",
        "airplane",
        "departure_time",
        "arrival_time",
        "status",
    )


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ("source", "destination", "distance", "code_route")


@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = ("name", "closest_big_city", "airport_code", "geographical_coordinates")


@admin.register(Airplane)
class AirplaneAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "airplane_type")


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ("airplane", "seat", "seat_type", "row", "ticket_class")


@admin.register(FlightSeat)
class FlightSeatAdmin(admin.ModelAdmin):
    list_display = ("seat", "flight")


@admin.register(AirplaneType)
class AirplaneTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Crew)
class CrewAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name")


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        "flight_seat",
        "order",
        "price",
    )


@admin.register(TicketClass)
class TicketClassAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "ticket_class")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("created_at", "user")
