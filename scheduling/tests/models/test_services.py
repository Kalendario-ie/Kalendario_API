from django.core.exceptions import ValidationError

from scheduling.models import Employee, Service
from scheduling.tests.generics import TestCaseWF


class ServiceTest(TestCaseWF):

    def test_add_employee(self):
        """Adding an employee to a service should be allowed where both entities belong to the same owner"""
        emp = Employee.objects.get(pk=2)
        service = Service.objects.get(pk=2)
        service.employee_set.add(emp)

        self.assertEquals(service.employee_set.get(pk=2), emp)

    def test_add_service_different_owner(self):
        """Adding an employee to a service with different owners in entities should raise an error"""
        service = Service.objects.get(pk=3)
        emp = Employee.objects.get(pk=2)

        self.assertRaises(ValidationError, service.employee_set.add, emp)

    def test_add_multiple_employees_different_owners(self):
        """Adding multiple employees to a service with different owners in entities should raise an error"""
        service = Service.objects.get(pk=3)
        employees = [Employee.objects.get(pk=2), Employee.objects.get(pk=1)]

        self.assertRaises(ValidationError, service.employee_set.add, *employees)

    def test_add_multiple_employees_mixed_owners(self):
        """Adding multiple employees to a service with mixed owners in entities should raise an error"""
        service = Service.objects.get(pk=3)
        employees = [Employee.objects.get(pk=2), Employee.objects.get(pk=5)]

        self.assertRaises(ValidationError, service.employee_set.add, *employees)