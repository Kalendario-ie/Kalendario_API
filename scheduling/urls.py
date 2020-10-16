from django.urls import path, include
from rest_framework import routers

from scheduling import views

router = routers.DefaultRouter()
router.register(r'employees', views.EmployeeViewSet, 'employee')
router.register(r'services', views.ServiceViewSet, 'service')
router.register(r'serviceCategories', views.ServiceCategoryViewSet, 'service-category')
router.register(r'schedules', views.ScheduleViewSet, 'schedule')
router.register(r'customers', views.CustomerViewSet, 'customer')
router.register(r'appointments', views.AppointmentViewSet, 'appointment')
router.register(r'requests', views.RequestViewSet, 'request')
router.register(r'companies', views.CompanyViewSet, 'company')
router.register(r'panels', views.SchedulingPanelViewSet, 'panel')

urlpatterns = [
    path(r'', include(router.urls)),
]
