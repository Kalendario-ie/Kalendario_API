from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration import views


class FacebookLogin(views.SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class FacebookConnect(views.SocialConnectView):
    adapter_class = FacebookOAuth2Adapter
