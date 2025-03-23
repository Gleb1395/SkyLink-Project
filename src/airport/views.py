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
    queryset = Airplane.objects.all().select_related("airplane_type")
    serializer_class = AirplaneListRetrieveSerializer

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return AirplaneListRetrieveSerializer
        return AirplaneCreateSerializer

    def get_queryset(self):
        name = self.request.GET.get("name")
        airplane_type = self.request.GET.get("airplane_type")
        queryset = self.queryset

        if name:
            queryset = queryset.filter(name__icontains=name)
        if airplane_type:
            queryset = queryset.filter(airplane_type__icontains=airplane_type)
        return queryset.distinct()


class SeatViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Seat.objects.all().select_related("airplane", "ticket_class", "airplane__airplane_type")

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return SeatListRetrieveSerializer
        return SeatCreateSerializer

    def get_queryset(self):
        airplane = self.request.GET.get("airplane")
        ticket_class = self.request.GET.get("ticket_class")
        queryset = self.queryset
        if airplane:
            queryset = queryset.filter(airplane__name__icontains=airplane)
        if ticket_class:
            queryset = queryset.filter(ticket_class__name__icontains=ticket_class)
        return queryset.distinct()


class OrderViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class TicketClassViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = TicketClass.objects.all()
    serializer_class = TicketClassSerializer


class TariffViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Tariff.objects.all().select_related("ticket_class")

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return TariffListRetrieveSerializer
        return TariffCreateSerializer

    def get_queryset(self):
        ticket_class = self.request.GET.get("ticket_class")
        code = self.request.GET.get("code")
        name = self.request.GET.get("name")
        queryset = self.queryset
        if ticket_class:
            queryset = queryset.filter(ticket_class__name__icontains=ticket_class)
        if code:
            queryset = queryset.filter(code__icontains=code)
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset.distinct()


class TicketViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Ticket.objects.all().select_related("flight_seat", "order")

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return TicketListRetrieveSerializer
        return TicketCreateSerializer


class AirportViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, GenericViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer


class RouteViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, GenericViewSet):
    queryset = Route.objects.all().select_related("source", "destination")

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return RouteListRetrieveSerializer
        return RouteCreateSerializer


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer


class FlightViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, GenericViewSet):
    queryset = Flight.objects.all().select_related("route", "airplane").prefetch_related("crew")

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return FlightListRetrieveSerializer
        return FlightCreateSerializer


class FlightSeatViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, GenericViewSet):
    queryset = FlightSeat.objects.all().select_related(
        "seat__airplane__airplane_type",
        "seat__ticket_class",
        "flight__route__source",
        "flight__route__destination",
        "flight__airplane__airplane_type",
    ).prefetch_related("flight__crew")

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return FlightSeatListRetrieveSerializer
        return FlightSeatCreateSerializer
