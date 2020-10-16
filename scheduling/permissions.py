from rest_framework import permissions


class EmployeeDashboardPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'employee') and request.user.employee is not None
