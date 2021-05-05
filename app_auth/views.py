from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from dj_rest_auth.registration import views
from rest_framework.permissions import IsAuthenticated
from allauth.account.utils import send_email_confirmation


class FacebookLogin(views.SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class FacebookConnect(views.SocialConnectView):
    adapter_class = FacebookOAuth2Adapter


class ResendEmail(views.APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        send_email_confirmation(request, request.user)
        return views.Response(
            {"detail": "Email Verification Resent"}
        )
