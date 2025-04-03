from django.http import HttpRequest, HttpResponse
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from airport.models import (Airplane, AirplaneType, Airport, Crew, Flight,
                            FlightSeat, Order, Route, Seat, Tariff, Ticket,
                            TicketClass)
from airport.permissions import IsAdminOrIfAuthenticatedReadOnly
from airport.serializers import (AirplaneCreateSerializer,
                                 AirplaneListRetrieveSerializer,
                                 AirplaneTypeSerializer, AirportSerializer,
                                 CrewSerializer, FlightCreateSerializer,
                                 FlightListRetrieveSerializer,
                                 FlightSeatCreateSerializer,
                                 FlightSeatListRetrieveSerializer,
                                 OrderSerializer, RouteCreateSerializer,
                                 RouteListRetrieveSerializer,
                                 SeatCreateSerializer, SeatFilterSerializer,
                                 SeatListRetrieveSerializer,
                                 TariffCreateSerializer,
                                 TariffFilterSerializer,
                                 TariffListRetrieveSerializer,
                                 TicketClassSerializer, TicketCreateSerializer,
                                 TicketListRetrieveSerializer)
from airport.services.convert_html_to_pdf import generate_and_send_pdf
from airport.tasks.mail import weekly_wish_email


class AirplaneTypeViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    """
    ViewSet for viewing (list, retrieve) and creating (create) airplane types.
    """

    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer


class AirplaneViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    """
    ViewSet for displaying a list, retrieving parts and creating airplanes.

    Supports filtering by airplane name (name) and airplane_type (airplane_type).
    Uses different serializers for reading (list, retrieve) and creating (create).
    """

    queryset = Airplane.objects.all().select_related("airplane_type")
    serializer_class = AirplaneListRetrieveSerializer

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return AirplaneListRetrieveSerializer
        return AirplaneCreateSerializer

    def get_queryset(self):
        """Retrieve the airplanes with filters"""
        name = self.request.GET.get("name")
        airplane_type = self.request.GET.get("airplane_type")
        queryset = self.queryset

        if name:
            queryset = queryset.filter(name__icontains=name)
        if airplane_type:
            queryset = queryset.filter(airplane_type__name__icontains=airplane_type)
        return queryset.distinct()

    @extend_schema(
        parameters=[
            OpenApiParameter(name="name", type=str, description="Filter by airplane name (partial match)"),
            OpenApiParameter(name="airplane_type", type=str, description="Filter by airplane type (partial match)"),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class SeatViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    """
    ViewSet for listing, retrieving and creating seats.

    Supports filtering by airplane name and ticket class name.
    Uses different serializers for reading and creating.
    """

    queryset = Seat.objects.all().select_related("airplane", "ticket_class", "airplane__airplane_type")
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return SeatListRetrieveSerializer
        return SeatCreateSerializer

    def get_queryset(self):
        """Retrieve the seats with filters"""

        airplane = self.request.GET.get("airplane")
        ticket_class = self.request.GET.get("ticket_class")

        queryset = self.queryset
        if airplane:
            queryset = queryset.filter(airplane__name__icontains=airplane)
        if ticket_class:
            queryset = queryset.filter(ticket_class__name__icontains=ticket_class)
        return queryset.distinct()

    @extend_schema(parameters=[SeatFilterSerializer])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class OrderViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class TicketClassViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = TicketClass.objects.all()
    serializer_class = TicketClassSerializer


class TariffViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    """
    ViewSet for managing tariffs.

    Supports listing, creating and retrieving fares.
    Added filters by ticket_class, code and name via query-parameters.
    """

    queryset = Tariff.objects.all().select_related("ticket_class").order_by("code")

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

    @extend_schema(parameters=[TariffFilterSerializer])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


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
    queryset = (
        FlightSeat.objects.all()
        .select_related(
            "seat__airplane__airplane_type",
            "seat__ticket_class",
            "flight__route__source",
            "flight__route__destination",
            "flight__airplane__airplane_type",
        )
        .prefetch_related("flight__crew")
    )

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return FlightSeatListRetrieveSerializer
        return FlightSeatCreateSerializer


@api_view(["GET"])
def send_ticket(request: HttpRequest) -> HttpResponse:
    user = request.user
    if not user.is_authenticated:
        return Response({"detail": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

    template_name = "ticket.html"

    tickets = Ticket.objects.filter(order__user=user).select_related(
        "flight_seat__flight__route__source",
        "flight_seat__flight__route__destination",
        "flight_seat__flight",
        "flight_seat__seat",
        "order__user",
        "order",
    )

    context = {"tickets": tickets}
    generate_and_send_pdf(user=user, template_name=template_name, context=context)

    return Response({"detail": "Ticket sent successfully"}, status=status.HTTP_200_OK)


@api_view(["GET"])
def send_to_user_weekly_email(request: HttpRequest) -> HttpResponse:
    weekly_wish_email.delay()
    return Response({"detail": "Email sent successfully"}, status=status.HTTP_200_OK)
