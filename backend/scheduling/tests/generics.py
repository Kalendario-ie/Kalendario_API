from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.test import TestCase

FIXTURES = ['companies.json', 'config.json', 'timeframes.json', 'shifts.json', 'schedules.json',
            'people.json', 'services.json', 'employees.json', 'customers.json',
            'users.json', 'requests.json', 'appointments.json']


class TestCaseWF(TestCase):
    """
    fixtures added to the test case
    """
    fixtures = FIXTURES


class ViewTestCase(APITestCase, TestCaseWF):
    list_url = None
    detail = None
    model = None

    def detail_url(self, model_id=None):
        if model_id is None:
            model_id = self.model.objects.first().id
        return reverse(self.detail, kwargs={'pk': model_id})

    def ensure_all_unauthorized(self):
        ensure_no_access(self, self.list_url, self.detail_url(), status.HTTP_401_UNAUTHORIZED)

    def ensure_all_forbidden(self, detail_url):
        ensure_no_access(self, self.list_url, detail_url, status.HTTP_403_FORBIDDEN)


def ensure_no_access(test_case, list_url, detail_url, response_status):
    response = test_case.client.get(list_url, format='json')
    test_case.assertEqual(response.status_code, response_status)

    response = test_case.client.post(list_url, format='json')
    test_case.assertEqual(response.status_code, response_status)

    response = test_case.client.get(detail_url, format='json')
    test_case.assertEqual(response.status_code, response_status)

    response = test_case.client.put(detail_url, format='json')
    test_case.assertEqual(response.status_code, response_status)

    response = test_case.client.patch(detail_url, format='json')
    test_case.assertEqual(response.status_code, response_status)

    response = test_case.client.delete(detail_url, format='json')
    test_case.assertEqual(response.status_code, response_status)
