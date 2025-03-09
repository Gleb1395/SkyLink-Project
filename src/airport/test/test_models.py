from django.contrib.auth import get_user_model
from django.test import TestCase

from airport.models import Crew, Order


class TestCrew(TestCase):
    def test_crew_format(self):
        test_crew = Crew.objects.create(first_name="Test", last_name="Crew")
        self.assertEqual(test_crew.first_name, "Test")
        self.assertEqual(test_crew.last_name, "Crew")
        self.assertEqual(str(test_crew), "Test Crew")


class TestOrder(TestCase):
    def test_order_format(self):
        username = "Test"
        email = "test@test.com"
        password = "password"
        test_user = get_user_model().objects.create(
            username=username,
            email=email,
            password=password,
        )
        order_test = Order.objects.create(user=test_user)
        self.assertEqual(str(order_test), f"Order date: {order_test.created_at}, User:{username}")
