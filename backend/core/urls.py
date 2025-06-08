from django.urls import path, include
from rest_framework import routers

from core import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, 'user')
router.register(r'groups', views.GroupProfileViewSet, 'group')

urlpatterns = [
    path(r'', include(router.urls))
]
