from django.urls import path
from core.views import UserViewSet

urlpatterns = [
    path(r'users/current/', UserViewSet.as_view(), name='current'),
]