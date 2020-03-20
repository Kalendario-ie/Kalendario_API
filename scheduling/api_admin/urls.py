from django.urls import path, include
from rest_framework import routers

import scheduling.api_admin.views as views

router = routers.DefaultRouter()
router.register(r'employees', views.EmployeeViewSet, base_name='employee')
router.register(r'services', views.ServiceViewSet, base_name='service')
router.register(r'shifts', views.ShiftViewSet, base_name='shift')
router.register(r'schedules', views.ScheduleViewSet, base_name='schedule')
router.register(r'customers', views.CustomerViewSet, base_name='customer')

urlpatterns = [
    path(r'', include(router.urls)),
]
