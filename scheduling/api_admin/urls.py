from django.urls import path, include
from rest_framework import routers

from scheduling.api_admin.views import EmployeeViewSet, ServiceViewSet

router = routers.DefaultRouter()
router.register(r'employees', EmployeeViewSet, base_name='employee')
router.register(r'services', ServiceViewSet, base_name='service')

urlpatterns = [
    path(r'', include(router.urls)),
]
