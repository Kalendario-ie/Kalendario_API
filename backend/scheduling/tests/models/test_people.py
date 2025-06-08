from django.core.exceptions import ValidationError

from scheduling.models import Person, Company, Customer, Employee, Service, Schedule
from scheduling.tests.generics import TestCaseWF


class PersonTest(TestCaseWF):

    def test_customer_employee_id_sequence(self):
        last_id = Person.objects.last().id
        company = Company.objects.first()
        customer = Customer(owner=company)
        emp = Employee(owner=company)
        customer.save(), emp.save()
        self.assertEqual(customer.id, last_id + 1)
        self.assertEqual(emp.id, customer.id + 1)


class CustomerTest(TestCaseWF):

    def test_create_customer(self):
        """
        When a new customer is created the variable for name should be set based on first name and last name
        """
        email = 'not_used_yet@test.com'
        c1 = Customer.objects.create(email=email, first_name='fname', last_name='lname', owner_id=1)
        self.assertEquals(c1.name, c1.first_name + ' ' + c1.last_name)

    def test_create_customer_same_email(self):
        """
            System should throw an error on an attempt to create a customer with the same email
                as another customer in that same company
        """
        email = 'not_used_yet@test.com'
        c1 = Customer.objects.create(email=email, owner_id=1)
        self.assertIsInstance(c1, Customer)
        self.assertRaises(ValidationError, Customer.objects.create, email=email, owner_id=1)

    def test_create_customer_same_email_different_company(self):
        """
            System should allow the same email address when the companies are different
        """
        email = 'not_used_yet@test.com'
        c1 = Customer.objects.create(email=email, owner_id=1)
        c2 = Customer.objects.create(email=email, owner_id=2)
        self.assertIsInstance(c1, Customer)
        self.assertIsInstance(c2, Customer)

    def test_saving_a_customer_should_not_throw_error(self):
        """
            System should allow the same email address when the companies are different
        """
        email = 'not_used_yet@test.com'
        c1 = Customer.objects.create(email=email, owner_id=1)
        c1.save()
        self.assertIsInstance(c1, Customer)


class EmployeeTest(TestCaseWF):

    def test_add_service(self):
        """Adding a service to an employee should be allowed where both entities belong to the same owner"""
        emp = Employee.objects.get(pk=2)
        service = Service.objects.get(pk=2)
        emp.services.add(service)

        self.assertEquals(emp.services.get(pk=2), service)

    def test_add_service_different_owner(self):
        """Adding a service to an employee with different owners in entities should raise an error"""
        emp = Employee.objects.get(pk=2)
        service = Service.objects.get(pk=3)

        self.assertRaises(ValidationError, emp.services.add, service)

    def test_add_multiple_services_different_owners(self):
        """Adding a service to an employee with different owners in entities should raise an error"""
        emp = Employee.objects.get(pk=2)
        services = [Service.objects.get(pk=3), Service.objects.get(pk=4)]

        self.assertRaises(ValidationError, emp.services.add, *services)

    def test_add_multiple_services_mixed_owners(self):
        """Adding a service to an employee with mixed owners in entities should raise an error"""
        emp = Employee.objects.get(pk=2)
        services = [Service.objects.get(pk=2), Service.objects.get(pk=4)]

        self.assertRaises(ValidationError, emp.services.add, *services)

    def test_changing_schedule(self):
        """
        Employees can only be assigned schedule from the same owner
        """
        emp = Employee.objects.get(pk=1)
        sch = Schedule.objects.get(pk=3)
        emp.schedule = sch
        emp.save()

        self.assertEquals(emp.schedule, sch)

    def test_changing_schedule_different_owner(self):
        """
        An error should be thrown
        When assigned to a schedule of a different owner
        """
        emp = Employee.objects.get(pk=1)
        sch = Schedule.objects.get(pk=2)
        emp.schedule = sch

        self.assertRaises(ValidationError, emp.save)