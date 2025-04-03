from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.test import TestCase

from airport.models import Order, Tariff, TicketClass


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
        self.assertEqual(str(order_test), f"Order date: {order_test.created_at}")


class TestTariff(TestCase):
    def setUp(self):
        self.ticket_class = TicketClass.objects.create(name="Test TicketClass")
        self.test_code = "A"
        self.test_name = "Test Tariff"
        self.tariff_test = Tariff.objects.create(
            code=self.test_code, name=self.test_name, ticket_class=self.ticket_class
        )

        self.assertEqual(
            str(self.tariff_test),
            f"Tariff code: {self.test_code}, "
            f"Tariff name: {self.test_name}, "
            f"Ticket class: {self.ticket_class.name}",
        )

    def test_tariff_uniq(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Tariff.objects.create(code=self.test_code, name=self.test_name, ticket_class=self.ticket_class)
