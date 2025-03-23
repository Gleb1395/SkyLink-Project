from rest_framework import serializers

from airport.models import (Airplane, AirplaneType, Airport, Crew, Flight,
                            FlightSeat, Order, Route, Seat, Tariff, Ticket,
                            TicketClass)


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = ("name",)


class AirplaneListRetrieveSerializer(serializers.ModelSerializer):
    airplane_type = serializers.SlugRelatedField(read_only=True, slug_field="name")

    class Meta:
        model = Airplane
        fields = ("name", "airplane_type")


class AirplaneCreateSerializer(AirplaneListRetrieveSerializer):
    airplane_type = serializers.PrimaryKeyRelatedField(queryset=AirplaneType.objects.all())


class SeatListRetrieveSerializer(serializers.ModelSerializer):
    airplane = serializers.SlugRelatedField(read_only=True, slug_field="name")
    ticket_class = serializers.SlugRelatedField(read_only=True, slug_field="name")

    class Meta:
        model = Seat
        fields = ("airplane", "seat", "row", "ticket_class")


class SeatCreateSerializer(SeatListRetrieveSerializer):
    airplane = serializers.PrimaryKeyRelatedField(queryset=Airplane.objects.all())
    ticket_class = serializers.PrimaryKeyRelatedField(queryset=TicketClass.objects.all())


class OrderSerializer(serializers.ModelSerializer):
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
    ticket_class = serializers.PrimaryKeyRelatedField(queryset=TicketClass.objects.all())


class TicketSerializer(serializers.ModelSerializer):
    flight_seat = serializers.PrimaryKeyRelatedField(queryset=FlightSeat.objects.all())

    class Meta:
        model = Ticket
        fields = ("order", "price", "flight_seat")


class TicketListRetrieveSerializer(TicketSerializer):
    order = OrderSerializer()


class TicketCreateSerializer(TicketSerializer):
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())
    flight_seat = serializers.PrimaryKeyRelatedField(queryset=FlightSeat.objects.all())


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ("name", "closest_big_city", "airport_code", "geographical_coordinates")


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ("source", "destination", "distance", "code_route")


class RouteListRetrieveSerializer(RouteSerializer):
    source = serializers.SlugRelatedField(
        slug_field="name",
        read_only=True,
    )
    destination = serializers.SlugRelatedField(
        slug_field="name",
        read_only=True,
    )


class RouteCreateSerializer(RouteSerializer):
    source = serializers.PrimaryKeyRelatedField(
        queryset=Airport.objects.all(),
    )
    destination = serializers.PrimaryKeyRelatedField(
        queryset=Airport.objects.all(),
    )


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ("first_name", "last_name")


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = (
            "route",
            "airplane",
            "departure_time",
            "arrival_time",
            "status",
        )


class FlightListRetrieveSerializer(FlightSerializer):
    route = RouteListRetrieveSerializer()
    crew = CrewSerializer(many=True, read_only=True)
    airplane = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    formatted_duration = serializers.SerializerMethodField()

    class Meta:
        model = Flight
        fields = ("route", "airplane", "departure_time", "arrival_time", "status", "crew", "formatted_duration")

    def get_airplane(self, obj):
        return obj.airplane.name

    def get_status(self, obj):
        status_mapping = {1: "SCHEDULED", 2: "DELAYED", 3: "CANCELLED", 4: "COMPLETED"}
        return status_mapping.get(obj.status, "UNKNOWN")

    def get_formatted_duration(self, obj):
        duration = obj.arrival_time - obj.departure_time
        hours, remainder = divmod(duration.total_seconds(), 3600)
        minutes, _ = divmod(remainder, 60)
        return f"{int(hours)}ч {int(minutes)}м"


class FlightCreateSerializer(FlightSerializer):
    crew = serializers.PrimaryKeyRelatedField(
        queryset=Crew.objects.all(),
        many=True,
        write_only=True,
    )

    class Meta:
        model = Flight
        fields = (
            "route",
            "airplane",
            "departure_time",
            "arrival_time",
            "status",
            "crew",
        )

    def create(self, validated_data):
        crew_data = validated_data.pop("crew", [])
        flight = Flight.objects.create(**validated_data)
        flight.crew.set(crew_data)
        return flight


class FlightSeatListRetrieveSerializer(serializers.ModelSerializer):
    seat = SeatListRetrieveSerializer()
    flight = FlightListRetrieveSerializer()

    class Meta:
        model = FlightSeat
        fields = ("seat", "flight")


class FlightSeatCreateSerializer(serializers.ModelSerializer):
    seat = serializers.PrimaryKeyRelatedField(
        queryset=Seat.objects.all(),
    )
    flight = serializers.PrimaryKeyRelatedField(
        queryset=Flight.objects.all(),
    )

    class Meta:
        model = FlightSeat
        fields = ("seat", "flight")
