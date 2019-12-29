from rest_framework import permissions


class ModelPermission(permissions.BasePermission):

    def __init__(self, action, model):
        self.action = action
        self.model = model

    def has_permission(self, request, view):
        return request.user.has_perm(f'scheduling.{self.action}_{self.model}')
