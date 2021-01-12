from rest_framework.permissions import BasePermission
from . import helpers


class StripeAuthentication(BasePermission):
    """
    Allows access only valid stripe requests to go trough
    """
    def has_permission(self, request, view):
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        try:
            view.kwargs['event'] = helpers.construct_event(request.data, sig_header, view.hook_secret)
            return True
        except ValueError as e:
            return False
