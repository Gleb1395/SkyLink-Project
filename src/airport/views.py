import os

from django.http import FileResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from playwright.sync_api import sync_playwright
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
from config import settings


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


def generate_ticket_pdf_by_seat(request):
    user = request.user
    if not user.is_authenticated:
        from django.http import HttpResponse

        return HttpResponse("Unauthorized", status=401)

    tickets = Ticket.objects.filter(order__user=user).select_related(
        "flight_seat__flight__route__source",
        "flight_seat__flight__route__destination",
        "flight_seat__flight",
        "flight_seat__seat",
        "order__user",
        "order",
    )

    context = {"tickets": tickets}

    html_string = render_to_string("index.html", context)

    static_root = os.path.join(settings.BASE_DIR, "static")
    static_url = f"file:///{static_root.replace(os.sep, '/')}"

    html_string = html_string.replace('href="/static/', f'href="{static_url}/')
    html_string = html_string.replace('src="/static/', f'src="{static_url}/')

    html_path = os.path.join(settings.BASE_DIR, "ticket_preview.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_string)

    pdf_path = os.path.join(settings.BASE_DIR, "ticket_output.pdf")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(f"file:///{html_path}", wait_until="networkidle")
        page.pdf(path=pdf_path, format="A4", print_background=True)
        browser.close()

    return FileResponse(open(pdf_path, "rb"), content_type="application/pdf")
