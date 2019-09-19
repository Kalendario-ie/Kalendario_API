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
