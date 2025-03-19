import os
import random
from datetime import datetime, timedelta

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.config.settings")
django.setup()

from faker import Faker

from airport.models import (Airplane, AirplaneType, Airport, Crew, Seat,
                            TicketClass, Route, Flight)


def create_test_crews(count: int) -> list[Crew]:
    fake = Faker()
    crews = [Crew(first_name=fake.first_name(), last_name=fake.last_name()) for _ in range(count)]
    return Crew.objects.bulk_create(crews)


def create_test_airplanes() -> None:
    passenger_plane, _ = AirplaneType.objects.get_or_create(name="Passenger plane")
    business_plane, _ = AirplaneType.objects.get_or_create(name="Business plane")

    passengers_plane_names = ["Boeing 737", "Airbus A320", "Embraer E190"]
    business_jet_list_names = ["Gulfstream G650", "Bombardier Global 7500", "Dassault Falcon 7X"]

    test_planes_passenger = [Airplane(name=name, airplane_type=passenger_plane) for name in passengers_plane_names]
    test_planes_business = [Airplane(name=name, airplane_type=business_plane) for name in business_jet_list_names]

    Airplane.objects.bulk_create(test_planes_passenger)
    Airplane.objects.bulk_create(test_planes_business)


def create_seat(airplane: Airplane, row, seat_number, ticket_class) -> Seat:
    return Seat(
        airplane=airplane,
        row=row,
        seat=seat_number,
        ticket_class=ticket_class,
    )


def create_tests_seat_for_airplanes() -> None:
    airplane = list(Airplane.objects.filter(airplane_type__name="Passenger plane"))

    first_plane, second_plane, third_plane, *_ = airplane

    ticket_class_first, _ = TicketClass.objects.get_or_create(name="First class")
    ticket_class_business, _ = TicketClass.objects.get_or_create(name="Business class")
    ticket_class_economy, _ = TicketClass.objects.get_or_create(name="Economy class")

    seats_to_create = []

    for seat_number in range(1, 11):
        for plane in [first_plane, second_plane, third_plane]:
            seats_to_create.append(create_seat(plane, "A", seat_number, ticket_class_first))

    for seat_number in range(2, 22):
        for plane in [first_plane, second_plane, third_plane]:
            seats_to_create.append(create_seat(plane, "B", seat_number, ticket_class_business))

    for seat_number in range(3, 33):
        for plane in [first_plane, second_plane, third_plane]:
            seats_to_create.append(create_seat(plane, "C", seat_number, ticket_class_economy))

    Seat.objects.bulk_create(seats_to_create)


def create_tests_airport(count: int) -> None:
    fake = Faker()

    for _ in range(count):
        airport = Airport(
            name=fake.name(),
            closest_big_city=fake.city(),
            airport_code=fake.country_code(),
            geographical_coordinates=fake.coordinate(),
        )
        airport.save()


def create_test_route(count: int) -> None:
    airports = list(Airport.objects.all())
    source_airport = airports[:len(airports) // 2]
    destination_airport = airports[len(airports) // 2:]
    fake = Faker()
    lists_route = []
    for _ in range(count):
        lists_route.append(
            Route(
                source=random.choice(source_airport),
                destination=random.choice(destination_airport),
                distance=random.randint(1, 100),
                code_route=fake.country_code(),
            )
        )
    Route.objects.bulk_create(lists_route)


def create_tests_flights(count: int) -> None:
    routes = list(Route.objects.all())
    airplanes = list(Airplane.objects.all())
    crews = list(Crew.objects.all())
    lists_flights = []
    for _ in range(count):
        lists_flights.append(
            Flight(
                route=random.choice(routes),
                airplane=random.choice(airplanes),
                departure_time=datetime.now(),
                arrival_time=datetime.now() + timedelta(hours=6),
                status=1,
            )
        )
    flights = Flight.objects.bulk_create(lists_flights)

    for flight in flights:
        crew_members = random.sample(crews,
                                     k=min(len(crews), random.randint(1, 5)))
        flight.crew.set(crew_members)

if __name__ == "__main__":
    create_test_crews(50)
    create_test_airplanes()
    create_tests_seat_for_airplanes()
    create_tests_airport(10)
    create_test_route(5)
    create_tests_flights(3)