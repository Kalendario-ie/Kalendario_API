from rest_framework import permissions


class CanViewEmployees(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('scheduling.view_employee')


class CanAddEmployees(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('scheduling.add_employee')


class CanChangeEmployees(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('scheduling.change_employee')


class CanDeleteEmployees(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('scheduling.delete_employee')


class CanViewServices(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('scheduling.view_service')


class CanAddServices(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('scheduling.add_service')


class CanChangeServices(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('scheduling.change_service')


class CanDeleteServices(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('scheduling.delete_service')


class CanViewShifts(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('scheduling.view_shift')


class CanAddShifts(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('scheduling.add_shift')


class CanChangeShifts(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('scheduling.change_shift')


class CanDeleteShifts(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('scheduling.delete_shift')

