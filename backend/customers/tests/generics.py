from django.test import TestCase
from rest_framework.test import APITestCase

FIXTURES = ['companies.json', 'people.json', 'services.json', 'timeframes.json', 'shifts.json', 'schedules.json',
            'users.json', 'customers.json', 'employees.json']


class TestCaseWF(TestCase):
    """
    fixtures added to the test case
    """
    fixtures = FIXTURES


class ViewTestCase(APITestCase, TestCaseWF):
    list_url = None
    fixtures = FIXTURES
