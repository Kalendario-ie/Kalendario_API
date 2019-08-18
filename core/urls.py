from django.urls import path, include
from rest_framework import routers
from core.views import UserViewSet, ObtainAuthUserView

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path(r'', include(router.urls)),
    path("auth/", ObtainAuthUserView.as_view(), name="auth_user"),
]