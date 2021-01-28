from django.core.exceptions import ValidationError
from django.db import IntegrityError

from scheduling.models import Company
from scheduling.tests.generics import TestCaseWF


class CompanyTest(TestCaseWF):

    def test_add_company_with_existing_name(self):
        """creating a company with the same name as another should not be allowed"""
        name = 'company-name'
        Company.objects.create(name=name)
        self.assertRaises(IntegrityError, Company.objects.create, name=name)

    def test_add_company_space_in_name(self):
        """company names shouldn't have spaces"""
        name = 'company with spaces'
        self.assertRaises(ValidationError, Company.objects.create, name=name)
        self.assertRaises(ValidationError, Company.objects.create, name=' startsWithSpace')

    def test_update_company_name_existing_name(self):
        """if the name of an already existing company is updated to a used name the company should fail on save"""
        name1 = 'company-1'
        name2 = 'company-2'
        Company.objects.create(name=name1)
        c2 = Company.objects.create(name=name2)
        c2.name = name1
        self.assertRaises(IntegrityError, c2.save)


class ConfigTest(TestCaseWF):
    pass