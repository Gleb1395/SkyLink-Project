from http.client import responses

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from airport.models import (Airplane, AirplaneType, Airport, Crew, Route, Seat,
                            Tariff, TicketClass)
from airport.serializers import (AirplaneListRetrieveSerializer,
                                 SeatListRetrieveSerializer,
                                 TariffListRetrieveSerializer)

AIRPLANES_URL = reverse("airport:airplane-list")
TARIFFS_URL = reverse("airport:tariff-list")
SEATS_URL = reverse("airport:seat-list")


class AirplanesListTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self._create_airplanes()

    def _create_airplanes(self):
        self.airplane_type_passenger = AirplaneType.objects.create(name="Passenger Jet")
        self.airplane_type_cargo = AirplaneType.objects.create(name="Cargo Plane")

        self.airplane_1 = Airplane.objects.create(name="Boeing 737", airplane_type=self.airplane_type_passenger)
        self.airplane_2 = Airplane.objects.create(name="Airbus A320", airplane_type=self.airplane_type_passenger)
        self.airplane_3 = Airplane.objects.create(name="Boeing 747-8F", airplane_type=self.airplane_type_cargo)
        self.airplane_4 = Airplane.objects.create(name="Antonov An-124 Ruslan", airplane_type=self.airplane_type_cargo)
        self.airplane_5 = Airplane.objects.create(name="Airbus A330-200F", airplane_type=self.airplane_type_cargo)

    def test_airplanes_list_success(self):
        """
        Test for successful retrieval of the airplane list.
        """
        response = self.client.get(AIRPLANES_URL)
        airplanes = Airplane.objects.all()
        serializer = AirplaneListRetrieveSerializer(airplanes, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_airplanes_filter_by_airplane_type(self):
        """
        A test of filtering airplanes by type.
        """
        response = self.client.get(
            AIRPLANES_URL,
            {
                "airplane_type": "Passenger Jet",
            },
        )

        airplanes_passenger = Airplane.objects.filter(airplane_type__name__icontains="Passenger Jet")
        serializer = AirplaneListRetrieveSerializer(airplanes_passenger, many=True)

        self.assertEqual(response.data, serializer.data)

    def test_airplanes_filter_by_airplane_type_and_name(self):
        """
        A test of filtering airplanes by type and name.
        """
        response = self.client.get(AIRPLANES_URL, {"airplane_type": "Cargo Plane", "name": "Boeing 747-8F"})
        airplanes = Airplane.objects.filter(
            airplane_type__name__icontains="Cargo Plane", name__icontains="Boeing 747-8F"
        )
        serializer = AirplaneListRetrieveSerializer(airplanes, many=True)

        self.assertEqual(response.data, serializer.data)

    def test_list_empty_database(self):
        """
        If there are no airplanes
        """
        Airplane.objects.all().delete()
        response = self.client.get(AIRPLANES_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_filter_no_match(self):
        """
        Filter found nothing
        """
        response = self.client.get(AIRPLANES_URL, {"name": "Boeing 123-456"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_filter_by_airplane_type_case_sensitive(self):
        """
        Filter by type with different case
        """
        response = self.client.get(AIRPLANES_URL, {"airplane_type": "paSSengEr jEt"})
        airplanes = Airplane.objects.filter(airplane_type__name__icontains="Passenger Jet")
        serializer = AirplaneListRetrieveSerializer(airplanes, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


class TariffsListTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self._create_tariff()

    def _create_tariff(self):
        self.ticket_class_first_class = TicketClass.objects.create(name="First class")
        self.ticket_class_business_class = TicketClass.objects.create(name="Business class")

        self.tariff_for_first_class_1 = Tariff.objects.create(
            code="A", name="standard fare", ticket_class=self.ticket_class_first_class
        )

        self.tariff_for_first_class_2 = Tariff.objects.create(
            code="B", name="first class at discounted price", ticket_class=self.ticket_class_business_class
        )

        self.tariff_for_first_class_3 = Tariff.objects.create(
            code="C", name="superior comfort fare", ticket_class=self.ticket_class_first_class
        )

        self.tariff_for_business_class_1 = Tariff.objects.create(
            code="D", name="tickets at discounted price", ticket_class=self.ticket_class_business_class
        )

        self.tariff_for_business_class_2 = Tariff.objects.create(
            code="E", name="tickets at discounted price", ticket_class=self.ticket_class_business_class
        )

        self.tariff_for_business_class_3 = Tariff.objects.create(
            code="F", name="standard fare", ticket_class=self.ticket_class_business_class
        )

    def test_tariffs_list_success(self):
        """
        Test for successful retrieval of the tariffs list.
        """
        response = self.client.get(TARIFFS_URL)
        tariffs = Tariff.objects.all().order_by("code")
        serializer = TariffListRetrieveSerializer(tariffs, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_tariffs_filter_by_code(self):
        """
        A test of filtering by code
        """

        response = self.client.get(TARIFFS_URL, {"code": "A"})

        tariffs = Tariff.objects.filter(code__icontains="A").order_by("code")
        serializer = TariffListRetrieveSerializer(tariffs, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_tariffs_filter_by_name(self):
        """
        A test of filtering by name
        """

        response = self.client.get(TARIFFS_URL, {"name": "standard fare"})

        tariffs = Tariff.objects.filter(name__icontains="standard fare").order_by("code")
        serializer = TariffListRetrieveSerializer(tariffs, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_tariffs_filter_by_ticket_class(self):
        """
        A test of filtering by ticket class
        """
        response = self.client.get(TARIFFS_URL, {"ticket_class": "First class"})

        tariffs = Tariff.objects.filter(ticket_class__name__icontains="First class").order_by("code")
        serializer = TariffListRetrieveSerializer(tariffs, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_tariffs_filter_by_code_and_name(self):
        """
        Test of filtering by code and name
        """
        response = self.client.get(TARIFFS_URL, {"code": "A", "name": "standard fare"})

        tariffs = Tariff.objects.filter(code__icontains="A", name__icontains="standard fare").order_by("code")
        serializer = TariffListRetrieveSerializer(tariffs, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_tariffs_filter_by_code_and_ticket_class(self):
        """
        Test of filtering by code and ticket class
        """
        response = self.client.get(TARIFFS_URL, {"code": "A", "ticket_class": "First class"})

        tariffs = Tariff.objects.filter(code__icontains="A", ticket_class__name__icontains="First class").order_by(
            "code"
        )
        serializer = TariffListRetrieveSerializer(tariffs, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_list_tariff_empty_database(self):
        """
        If there are no airplanes
        """

        Tariff.objects.all().delete()

        response = self.client.get(TARIFFS_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_filter_no_match_for_tariff(self):
        """
        Filter found nothing
        """

        response = self.client.get(TARIFFS_URL, {"code": "P"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_filter_by_airplane_type_case_sensitive(self):
        """
        Filter by type with different case
        """
        response = self.client.get(TARIFFS_URL, {"code": "a", "ticket_class": "firST cLaSs"})

        tariffs = Tariff.objects.filter(code__icontains="A", ticket_class__name__icontains="First class").order_by(
            "code"
        )
        serializer = TariffListRetrieveSerializer(tariffs, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


# class SeatListTest(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self._create_seats()
#
#     def _create_seats(self):
#         self.airplane_type_passenger = AirplaneType.objects.create(name="Passenger Jet")
#         self.airplane_1 = Airplane.objects.create(name="Boeing 737", airplane_type=self.airplane_type_passenger)
#
#         self.ticket_class_first_class = TicketClass.objects.create(name="First class")
#
#         self.seat_1 = Seat.objects.create(
#             airplane=self.airplane_1, seat=1, row="A", ticket_class=self.ticket_class_first_class
#         )
#         self.seat_2 = Seat.objects.create(
#             airplane=self.airplane_1, seat=2, row="A", ticket_class=self.ticket_class_first_class
#         )
#         self.seat_3 = Seat.objects.create(
#             airplane=self.airplane_1, seat=3, row="A", ticket_class=self.ticket_class_first_class
#         )
#
#         self.seat_4 = Seat.objects.create(
#             airplane=self.airplane_1, seat=4, row="B", ticket_class=self.ticket_class_first_class
#         )
#         self.seat_5 = Seat.objects.create(
#             airplane=self.airplane_1, seat=5, row="B", ticket_class=self.ticket_class_first_class
#         )
#         self.seat_6 = Seat.objects.create(
#             airplane=self.airplane_1, seat=6, row="B", ticket_class=self.ticket_class_first_class
#         )
#
#     def test_seats_list_success(self):
#         """
#         Test for successful retrieval of the seats list.
#         """
#         response = self.client.get(SEATS_URL)
#
#         seats = Seat.objects.all()
#         serializer = SeatListRetrieveSerializer(seats, many=True)
#
#         print(response.data)
#         print(serializer.data)
#
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data, serializer.data)
