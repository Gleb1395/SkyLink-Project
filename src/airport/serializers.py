from rest_framework import serializers

from airport.models import Airplane, AirplaneType, Tariff, TicketClass, Seat, Order, Ticket, FlightSeat


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = ("name",)


class AirplaneListRetrieveSerializer(serializers.ModelSerializer):
    airplane_type = serializers.SlugRelatedField(
        read_only=True,
        slug_field="name"
    )

    class Meta:
        model = Airplane
        fields = ("name", "airplane_type")


class AirplaneCreateSerializer(AirplaneListRetrieveSerializer):
    airplane_type = serializers.PrimaryKeyRelatedField(
        queryset=AirplaneType.objects.all()
    )


class SeatListRetrieveSerializer(serializers.ModelSerializer):
    airplane = serializers.SlugRelatedField(
        read_only=True,
        slug_field="name"
    )
    ticket_class = serializers.SlugRelatedField(
        read_only=True,
        slug_field="name"
    )

    class Meta:
        model = Seat
        fields = ("airplane", "seat", "row", "ticket_class")


class SeatCreateSerializer(SeatListRetrieveSerializer):
    airplane = serializers.PrimaryKeyRelatedField(
        queryset=Airplane.objects.all()
    )
    ticket_class = serializers.PrimaryKeyRelatedField(
        queryset=TicketClass.objects.all()
    )


class OrderListRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("created_at", "user")


class TicketClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketClass
        fields = ("name",)


class TariffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tariff
        fields = ("code", "name", "ticket_class")


class TariffListRetrieveSerializer(TariffSerializer):
    ticket_class = serializers.SlugRelatedField(
        slug_field="name",
        read_only=True,
    )


class TariffCreateSerializer(TariffSerializer):
    ticket_class = serializers.PrimaryKeyRelatedField(
        queryset=TicketClass.objects.all()
    )


class FlightSeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlightSeat
        fields = ("seat", "flight")


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("order", "price", "flight_seat")


class TicketListRetrieveSerializer(TicketSerializer):
    order = OrderListRetrieveSerializer()


class TicketCreateSerializer(TicketSerializer):
    order = serializers.PrimaryKeyRelatedField(
        queryset=Order.objects.all()
    )
    flight_seat = serializers.PrimaryKeyRelatedField(
        queryset=TicketClass.objects.all()
    )
