from django.urls import path, include
from rest_framework import routers

from airport.views import AirplaneTypeViewSet, AirplaneViewSet, SeatViewSet, OrderViewSet, TicketClassViewSet, \
    TariffViewSet, TicketViewSet

router = routers.DefaultRouter()

router.register("airplane-types", AirplaneTypeViewSet)
router.register("airplanes", AirplaneViewSet)
router.register("seats", SeatViewSet)
router.register("orders", OrderViewSet)
router.register("ticket-classes", TicketClassViewSet)
router.register("tariffs", TariffViewSet)
router.register("tickets", TicketViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "airport"
