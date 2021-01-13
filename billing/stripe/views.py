from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from . import helpers


class StripeHookView(APIView):
    hook_secret = None
    hook_handler_class = None

    def get_event(self):
        sig_header = self.request.META['HTTP_STRIPE_SIGNATURE']
        return helpers.construct_event(self.request.stream.body, sig_header, self.hook_secret)

    def post(self, request, *args, **kwargs):
        """
        Returns 200 if everything went ok
        422 if the event type has no handler
        404 if the event doesn't belong to a know entity
        """
        try:
            event = self.get_event()
        except ValueError as e:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        handler = self.hook_handler_class(event)

        if handler.invalid_event:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        if not handler.handle():
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_200_OK)
