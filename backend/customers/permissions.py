from rest_framework import permissions


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
    return set_field.filter(id=pk).exists()


class CanCreateAppointment(permissions.BasePermission):

    def has_permission(self, request, view):
        customer, user = int(request.data.get('customer', 0)), request.user

        return user.person and user.person.id == customer


class CanCreateCompany(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.owner:
            return False
        return True
