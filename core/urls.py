from django.urls import path
from core.views import CurrentUserViewSet, FacebookConnect, FacebookLogin, UserPermissionsViewSet

urlpatterns = [
    path(r'users/current/', CurrentUserViewSet.as_view(), name='current'),
    path(r'users/current/permissions/', UserPermissionsViewSet.as_view(), name='permissions'),
    path(r'auth/facebook/', FacebookLogin.as_view(), name='fb-login'),
    path(r'auth/facebook/connect/', FacebookConnect.as_view(), name='fb_connect'),
]
