from django.core.exceptions import ValidationError
from django.db import IntegrityError

from core import models
from core.tests.generics import TestCaseWF
from django.contrib.auth.models import Permission, Group


def create_group(owner_id):
    group = models.GroupProfile.objects.create(name='Testing', owner_id=owner_id)
    group.permissions.add(*Permission.objects.filter(codename='add_company'))
    group.save()
    return group


def get_user():
    return models.User.objects.get(pk=1)


class ProfileTest(TestCaseWF):

    def setUp(self):
        self.user = get_user()
        self.assertEqual(len(self.user.get_all_permissions()), 0)

    def add_group(self, group):
        self.user.groups.add(group.group)
        self.user.save()

    def assert_permissions_len(self, length):
        user = get_user()
        permission = list(user.get_all_permissions())
        self.assertEqual(len(permission), length)

    def test_profile_to_user(self):
        self.add_group(create_group(1))
        self.assert_permissions_len(1)

    def test_add_profile_different_company(self):
        self.assertRaises(ValidationError, self.add_group, create_group(2))


class UserTest(TestCaseWF):

    def test_create_user(self):
        email = 'ice.king@advtime.com'
        user = models.User.objects.create(first_name='Ice', last_name='King', email=email)
        self.assertEqual(user.email, email)

    def test_create_user_same_mail(self):
        email = 'ice.king@advtime.com'
        models.User.objects.create(first_name='Ice', last_name='King', email=email)
        self.assertRaises(IntegrityError, models.User.objects.create,
                          first_name='Ice', last_name='King', email=email)

    def test_update_user_existing_mail(self):
        email1 = 'ice.king@advtime.com'
        email2 = 'ice.king2@advtime.com'
        models.User.objects.create(first_name='Ice', last_name='King', email=email1)
        user2 = models.User.objects.create(first_name='Ice', last_name='King', email=email2)
        user2.email = email1
        self.assertRaises(IntegrityError, user2.save)

    def test_enable_company_editing(self):
        user = models.User.objects.first()
        user.enable_company_editing(1)
        group = user.groups.first()
        permissions = list(group.permissions.all())
        for permission in models.permissions():
            self.assertIn(permission, permissions)
