from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from airport.models import (Airplane, AirplaneType, Order, Seat, Tariff,
                            Ticket, TicketClass)
from airport.serializers import (AirplaneCreateSerializer,
                                 AirplaneListRetrieveSerializer,
                                 AirplaneTypeSerializer,
                                 OrderListRetrieveSerializer,
                                 SeatCreateSerializer,
                                 SeatListRetrieveSerializer,
                                 TariffCreateSerializer,
                                 TariffListRetrieveSerializer,
                                 TicketClassSerializer, TicketCreateSerializer,
                                 TicketListRetrieveSerializer,
                                 TicketSerializer)


class AirplaneTypeViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer


class AirplaneViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneListRetrieveSerializer

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return AirplaneListRetrieveSerializer
        return AirplaneCreateSerializer


class SeatViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Seat.objects.all()

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return SeatListRetrieveSerializer
        return SeatCreateSerializer


class OrderViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Order.objects.all()

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return OrderListRetrieveSerializer


class TicketClassViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = TicketClass.objects.all()
    serializer_class = TicketClassSerializer


class TariffViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Tariff.objects.all()

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return TariffListRetrieveSerializer
        return TariffCreateSerializer


class TicketViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Ticket.objects.all()

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return TicketListRetrieveSerializer
        return TicketCreateSerializer  # TODO Check it tomorrow
