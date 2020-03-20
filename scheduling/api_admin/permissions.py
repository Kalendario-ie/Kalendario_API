from rest_framework import permissions


def ModelPermissionFactory(action, model):
    class ModelPermission(permissions.BasePermission):
        def has_permission(self, request, view):
            return request.user.has_perm(f'scheduling.{action}_{model}')
    return ModelPermission


class IsCompanyAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.data.get('owner') == request.user.company_id is not None
