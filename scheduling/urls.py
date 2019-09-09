from django.urls import include, path
from rest_framework import routers
from scheduling.customer.views import CustomerAppointmentViewSet
from scheduling.employee.views import EmployeeAppointmentViewSet
from scheduling.views import EmployeeViewSet, CustomerViewSet, SelfAppointmentViewSet

router = routers.DefaultRouter()
router.register(r'employees', EmployeeViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'appointments', CustomerAppointmentViewSet, base_name='c-appointment')

router.register(r'admin/appointments', EmployeeAppointmentViewSet, base_name='e-appointment')
router.register(r'admin/self-appointments', SelfAppointmentViewSet, base_name='e-self-appointment')


urlpatterns = [
    path(r'', include(router.urls)),
    path(r'', include('rest_framework.urls', namespace='rest_framework')),
]
