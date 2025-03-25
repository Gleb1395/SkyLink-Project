from django.urls import include, path
from rest_framework import routers

from airport.views import (AirplaneTypeViewSet, AirplaneViewSet,
                           AirportViewSet, CrewViewSet, FlightSeatViewSet,
                           FlightViewSet, OrderViewSet, RouteViewSet,
                           SeatViewSet, TariffViewSet, TicketClassViewSet,
                           TicketViewSet, generate_ticket_pdf_by_seat)

router = routers.DefaultRouter()

router.register("airplane-types", AirplaneTypeViewSet)
router.register("airplanes", AirplaneViewSet)
router.register("seats", SeatViewSet)
router.register("orders", OrderViewSet)
router.register("ticket-classes", TicketClassViewSet)
router.register("tariffs", TariffViewSet)
router.register("tickets", TicketViewSet)  # TODO Сделать показ билетов только для конкретного User
router.register("airports", AirportViewSet)
router.register("routes", RouteViewSet)
router.register("crews", CrewViewSet)
router.register("flights", FlightViewSet)
router.register("flight-seats", FlightSeatViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("generate-ticket/", generate_ticket_pdf_by_seat, name="generate_ticket_pdf_by_seat"),
]

app_name = "airport"
