from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase

from airport.models import (Airplane, AirplaneType, Airport, Crew, Flight,
                            FlightSeat, Order, Route, Seat, Tariff, Ticket,
                            TicketClass)


class FlightModelTest(TestCase):
    def setUp(self):
        self.ticket_class = TicketClass.objects.create(
            name="Business",
        )
        self.tariff = Tariff.objects.create(
            code="A",
            name="Discount",
            ticket_class=self.ticket_class,
        )
        self.airplane_type = AirplaneType.objects.create(
            name="Boing 737",
        )
        self.airplane = Airplane.objects.create(
            name="Test Airplane",
            airplane_type=self.airplane_type,
        )
        self.seats_1 = Seat.objects.create(
            airplane=self.airplane,
            seat=1,
            row=1,
            seat_type="window",
            ticket_class=self.ticket_class,
        )
        self.seats_2 = Seat.objects.create(
            airplane=self.airplane,
            seat=2,
            row=1,
            seat_type="window",
            ticket_class=self.ticket_class,
        )
        self.seats_3 = Seat.objects.create(
            airplane=self.airplane,
            seat=3,
            row=1,
            seat_type="window",
            ticket_class=self.ticket_class,
        )
        self.crew_1 = Crew.objects.create(first_name="Test crew first name 1", last_name="Test crew last name 1")
        self.crew_2 = Crew.objects.create(first_name="Test crew first name 2", last_name="Test crew last name 2")
        self.airport_1 = Airport.objects.create(
            name="Charles De Gaulle Airport",
            closest_big_city="Paris",
            airport_code="FC",
            geographical_coordinates=1.2,
        )
        self.airport_2 = Airport.objects.create(
            name="John F. Kennedy International Airport",
            closest_big_city="New York",
            airport_code="KJFK",
            geographical_coordinates=5.6,
        )
        self.route = Route.objects.create(
            source=self.airport_1, destination=self.airport_2, distance=5000, code_route="AA"
        )
        self.flight_1 = Flight.objects.create(
            route=self.route,
            airplane=self.airplane,
            departure_time=datetime.now(),
            arrival_time=datetime.now() + timedelta(hours=6),
            status=1,
        )
        self.flight_seat_1 = FlightSeat.objects.create(
            seat=self.seats_1,
            flight=self.flight_1,
        )
        self.flight_seat_2 = FlightSeat.objects.create(
            seat=self.seats_2,
            flight=self.flight_1,
        )
        self.flight_seat_3 = FlightSeat.objects.create(
            seat=self.seats_3,
            flight=self.flight_1,
        )
        self.user = get_user_model().objects.create_user(
            username="TestUser", email="test@example.com", password="password123"
        )
        self.order = Order.objects.create(user=self.user)
        self.ticket_1 = Ticket.objects.create(
            order=self.order,
            price=10,
            flight_seat=self.flight_seat_1,
        )
        self.ticket_2 = Ticket.objects.create(
            order=self.order,
            price=11,
            flight_seat=self.flight_seat_2,
        )

    def test_with_available_seats(self):
        flight = Flight.objects.with_available_seats().get(id=1)
        self.assertEqual(flight.booked_seats, 2)
        self.assertEqual(flight.total_seats, 3)
        Seat.objects.create(
            airplane=self.airplane,
            seat=4,
            row=1,
            seat_type="window",
            ticket_class=self.ticket_class,
        )
        Ticket.objects.create(
            order=self.order,
            price=11,
            flight_seat=self.flight_seat_3,
        )
        flight = Flight.objects.with_available_seats().get(id=1)
        self.assertEqual(flight.booked_seats, 3)
        self.assertEqual(flight.total_seats, 4)
