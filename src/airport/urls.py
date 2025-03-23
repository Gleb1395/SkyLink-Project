from django.urls import include, path
from rest_framework import routers

from airport.views import (AirplaneTypeViewSet, AirplaneViewSet,
                           AirportViewSet, CrewViewSet, FlightSeatViewSet,
                           FlightViewSet, OrderViewSet, RouteViewSet,
                           SeatViewSet, TariffViewSet, TicketClassViewSet,
                           TicketViewSet)

router = routers.DefaultRouter()

router.register("airplane-types", AirplaneTypeViewSet)
router.register("airplanes", AirplaneViewSet)
router.register("seats", SeatViewSet)  # TODO Сделать фильтрацию и добавить select prefetch related
router.register("orders", OrderViewSet)  # TODO Сделать фильтрацию и добавить select prefetch related
router.register("ticket-classes", TicketClassViewSet)  # TODO Сделать фильтрацию и добавить select prefetch related
router.register("tariffs", TariffViewSet)  # TODO Сделать фильтрацию и добавить select prefetch related
router.register("tickets", TicketViewSet)  # TODO Сделать фильтрацию и добавить select prefetch related
router.register("airports", AirportViewSet)  # TODO Сделать фильтрацию и добавить select prefetch related
router.register("routes", RouteViewSet)  # TODO Сделать фильтрацию и добавить select prefetch related
router.register("crews", CrewViewSet)  # TODO Сделать фильтрацию и добавить select prefetch related
router.register("flights", FlightViewSet)  # TODO Сделать фильтрацию и добавить select prefetch related
router.register("flight-seats", FlightSeatViewSet)  # TODO Сделать фильтрацию и добавить select prefetch related

urlpatterns = [path("", include(router.urls))]

app_name = "airport"
