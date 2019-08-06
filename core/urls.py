from django.urls import path
from core.views import CurrentUserView, ObtainAuthUserView

urlpatterns = [
    path("users/current/", CurrentUserView.as_view(), name="current_user"),
    path("auth/", ObtainAuthUserView.as_view(), name="auth_user"),
]