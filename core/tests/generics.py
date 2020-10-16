from django.test import TestCase
from rest_framework.test import APITestCase

FIXTURES = ['people.json', 'companies.json', 'groups.json', 'groupprofiles.json', 'users.json']


class TestCaseWF(TestCase):
    """
    fixtures added to the test case
    """
    fixtures = FIXTURES


class ViewTestCase(APITestCase, TestCaseWF):
    list_url = None
    fixtures = FIXTURES
