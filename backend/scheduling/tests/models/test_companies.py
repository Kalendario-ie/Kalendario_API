from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from scheduling.tests import factories


class CompanyTest(TestCase):

    def create_fakes(self):
        self.company_a = factories.CompanyFactory.create()
        self.company_b = factories.CompanyFactory.create()
        for i in range(2):
            factories.EmployeeFactory.create(owner=self.company_a)
            factories.ServiceFactory.create(owner=self.company_a)
            factories.EmployeeFactory.create(owner=self.company_b)
            factories.ServiceFactory.create(owner=self.company_b)

        self.company_a_private_emp = factories.ServiceFactory.create(owner=self.company_a, private=True)

    def test_add_company_with_existing_name(self):
        """creating a company with the same name as another should not be allowed"""
        name = 'company name'
        factories.CompanyFactory.create(name=name)
        self.assertRaises(IntegrityError, factories.CompanyFactory.create, name=name)

    def test_add_company_underscore_in_name(self):
        """company names shouldn't have spaces"""
        self.assertRaises(ValidationError, factories.CompanyFactory.create, name='company_with_underscores')
        self.assertRaises(ValidationError, factories.CompanyFactory.create, name='_starts with underscore')
        self.assertRaises(ValidationError, factories.CompanyFactory.create, name='ends with underscore_')

    def test_update_company_name_existing_name(self):
        """if the name of an already existing company is updated to a used name the company should fail on save"""
        name1 = 'company-1'
        name2 = 'company-2'
        factories.CompanyFactory.create(name=name1)
        c2 = factories.CompanyFactory.create(name=name2)
        c2.name = name1
        self.assertRaises(IntegrityError, c2.save)

    def test_company_slug(self):
        name = 'Company with spaces'
        slug = 'Company_with_spaces'
        company = factories.CompanyFactory.create(name=name)
        self.assertEqual(company.slug, slug)

    def test_company_string_format(self):
        company = factories.CompanyFactory.create()
        self.assertEqual(str(company), company.name)

    def test_employee_list(self):
        """Ensures that the employee list doesn't contain private items or items from a different company"""
        company_a = factories.CompanyFactory.create()
        company_b = factories.CompanyFactory.create()

        for i in range(2):
            factories.EmployeeFactory.create(owner=company_a)
            factories.EmployeeFactory.create(owner=company_a, private=True)
            factories.EmployeeFactory.create(owner=company_b)
            factories.EmployeeFactory.create(owner=company_b, private=True)

        self.assertEqual(len(company_a.employees), 2)
        for emp in company_a.employees:
            self.assertEqual(emp.owner_id, company_a.id)
            self.assertFalse(emp.private)

    def test_service_list(self):
        """Ensures that the service list doesn't contain private items or items from a different company"""
        company_a = factories.CompanyFactory.create()
        company_b = factories.CompanyFactory.create()

        for i in range(2):
            factories.ServiceFactory.create(owner=company_a)
            factories.ServiceFactory.create(owner=company_a, private=True)
            factories.ServiceFactory.create(owner=company_b)
            factories.ServiceFactory.create(owner=company_b, private=True)

        self.assertEqual(len(company_a.services), 2)
        for service in company_a.services:
            self.assertEqual(service.owner_id, company_a.id)
            self.assertFalse(service.private)

    def test_config_can_receive_payment(self):
        company = factories.CompanyFactory.create()
        self.assertEqual(company.config.can_receive_unpaid_request, company.config.allow_unpaid_request)

    def test_config_can_receive_card_payments(self):
        company = factories.CompanyFactory.create()
        self.assertEqual(company.config.can_receive_card_payments,
                         company.account.is_stripe_enabled and company.config.allow_card_payment)
