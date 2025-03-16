from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from airport.models import Airplane, AirplaneType, Seat, Order, TicketClass, Tariff, Ticket
from airport.serializers import AirplaneTypeSerializer, AirplaneListRetrieveSerializer, AirplaneCreateSerializer, \
    SeatListRetrieveSerializer, SeatCreateSerializer, OrderListRetrieveSerializer, TariffListRetrieveSerializer, \
    TariffCreateSerializer, TicketClassSerializer, TicketSerializer, TicketListRetrieveSerializer, \
    TicketCreateSerializer


class AirplaneTypeViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet
):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer


class AirplaneViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet
):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneListRetrieveSerializer

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return AirplaneListRetrieveSerializer
        return AirplaneCreateSerializer


class SeatViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet
):
    queryset = Seat.objects.all()

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return SeatListRetrieveSerializer
        return SeatCreateSerializer


class OrderViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet
):
    queryset = Order.objects.all()

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return OrderListRetrieveSerializer


class TicketClassViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet
):
    queryset = TicketClass.objects.all()
    serializer_class = TicketClassSerializer


class TariffViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet
):
    queryset = Tariff.objects.all()

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return TariffListRetrieveSerializer
        return TariffCreateSerializer



class TicketViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet
):
    queryset = Ticket.objects.all()

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return TicketListRetrieveSerializer
        return TicketCreateSerializer # TODO Check it tomorrow