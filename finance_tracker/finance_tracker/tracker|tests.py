from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from .models import Transaction, SavingGoal
from django.urls import reverse
from decimal import Decimal
from datetime import date, timedelta

class BasicSmokeTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="tester", password="testpass")
        self.client.login(username="tester", password="testpass")  # session auth not used by JWT tests, but fine for simple checks

    def test_register_endpoint(self):
        resp = self.client.post(reverse("register"), {"username": "newu", "password": "abc123"})
        self.assertEqual(resp.status_code, 201)

    # note: deep JWT auth tests are omitted for brevity
