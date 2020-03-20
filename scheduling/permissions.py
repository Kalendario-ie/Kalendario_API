from rest_framework import permissions


class IsCustomer(permissions.BasePermission):
    """
    Checks if the user is a customer
    """

    def has_permission(self, request, view):
        return request.user.is_customer()


class IsEmployee(permissions.BasePermission):
    """
    Checks if the user is an employee
    """

    def has_permission(self, request, view):
        return request.user.is_employee() or request.user.has_perm('scheduling.view_appointment')


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.owner == request.user.person


def _check_if_exists(set_field, pk):
    if pk == 0:
        return True
    return len(set_field.filter(id=pk)) > 0


class CanCreateAppointment(permissions.BasePermission):

    def has_permission(self, request, view):
        customer, employee = int(request.data.get('customer', 0)), int(request.data.get('employee', 0))
        user, c = request.user, request.user.company

        if (user.is_company_admin()
                and _check_if_exists(c.employee_set, employee)
                and (_check_if_exists(c.customer_set, customer) or _check_if_exists(c.employee_set, customer))):
            return True

        # Make sure that the user is in the appointment
        if user.person and user.person.id in [customer, employee]:
            return True

        return False


class CanCreateCompany(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.company:
            return False
        return True
