from django.urls.exceptions import NoReverseMatch
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from billing import models

from core.models import User


class TestStripeViewSet(APITestCase):

    fixtures = ['companies.json', 'users.json']

    def list_detail_post_results(self, owner_id):
        detail_url = reverse('company-stripe-detail', kwargs={'owner_id': owner_id})
        get_detail = self.client.get(detail_url, format='json')
        post = self.client.post(detail_url + 'url/', format='json')
        return get_detail, post

    def test_list_url_does_not_exist(self):
        self.assertRaises(NoReverseMatch, reverse, 'company-stripe-list')

    def test_anonymous_users_access(self):
        """
        Anonymous users should have no access
        """
        get_detail, post = self.list_detail_post_results(1)

        self.assertEqual(get_detail.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(post.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_access_own_company(self):
        """
        A user should not be able to access the view when trying to see a different company
        """
        user = User.objects.get(pk=1)

        self.client.force_authenticate(user)
        get_detail, post = self.list_detail_post_results(1)

        self.assertEqual(get_detail.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(post.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_with_rights_access_own_company(self):
        """
        A user that has read/write rights to StripeConnectedAccount should be able to access the views
        """

        user = User.objects.get(pk=1)
        user.add_permissions(models.StripeAccount)

        self.client.force_authenticate(user)
        get_detail, post = self.list_detail_post_results(1)

        self.assertEqual(get_detail.status_code, status.HTTP_200_OK)
        self.assertEqual(post.status_code, status.HTTP_200_OK)

    def test_user_access_to_different_company(self):
        """
        A user should not be able to access the view when trying to see a different company
        """
        user = User.objects.get(pk=1)
        user.add_permissions(models.StripeAccount)

        self.client.force_authenticate(user)
        get_detail, post = self.list_detail_post_results(2)

        self.assertEqual(get_detail.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(post.status_code, status.HTTP_404_NOT_FOUND)
