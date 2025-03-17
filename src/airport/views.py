from rest_framework import mixins, viewsets
from rest_framework.viewsets import GenericViewSet

from airport.models import (Airplane, AirplaneType, Airport, Crew, Flight,
                            FlightSeat, Order, Route, Seat, Tariff, Ticket,
                            TicketClass)
from airport.serializers import (AirplaneCreateSerializer,
                                 AirplaneListRetrieveSerializer,
                                 AirplaneTypeSerializer, AirportSerializer,
                                 CrewSerializer, FlightCreateSerializer,
                                 FlightListRetrieveSerializer,
                                 FlightSeatCreateSerializer,
                                 FlightSeatListRetrieveSerializer,
                                 OrderSerializer, RouteCreateSerializer,
                                 RouteListRetrieveSerializer,
                                 SeatCreateSerializer,
                                 SeatListRetrieveSerializer,
                                 TariffCreateSerializer,
                                 TariffListRetrieveSerializer,
                                 TicketClassSerializer, TicketCreateSerializer,
                                 TicketListRetrieveSerializer)


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


class OrderViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


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


class AirportViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, GenericViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer


class RouteViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, GenericViewSet):
    queryset = Route.objects.all()

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return RouteListRetrieveSerializer
        return RouteCreateSerializer


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer


class FlightViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, GenericViewSet):
    queryset = Flight.objects.all()

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return FlightListRetrieveSerializer
        return FlightCreateSerializer


class FlightSeatViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, GenericViewSet):
    queryset = FlightSeat.objects.all()

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return FlightSeatListRetrieveSerializer
        return FlightSeatCreateSerializer
