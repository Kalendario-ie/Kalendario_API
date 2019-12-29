from django.urls import path, include
from rest_framework import routers

from scheduling.api_admin.views import EmployeeViewSet, ServiceViewSet, ShiftViewSet

router = routers.DefaultRouter()
router.register(r'employees', EmployeeViewSet, base_name='employee')
router.register(r'services', ServiceViewSet, base_name='service')
router.register(r'shifts', ShiftViewSet, base_name='shift')

urlpatterns = [
    path(r'', include(router.urls)),
]
