from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from airport.models import Airplane, AirplaneType
from airport.serializers import AirplaneListRetrieveSerializer

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
