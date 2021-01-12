from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from billing.stripe.authentication import StripeAuthentication


class StripeHookView(APIView):
    permission_classes = [StripeAuthentication]
    hook_secret = None
    hook_handler_class = None

    def post(self, request, event):
        """
        Returns 200 if everything went ok
        422 if the event type has no handler
        404 if the event doesn't belong to a know entity
        """
        handler = self.hook_handler_class(event)

        if handler.invalid_event:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        if not handler.handle():
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_200_OK)
