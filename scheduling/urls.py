from django.urls import include, path
from rest_framework import routers
from scheduling.customer.views import CustomerAppointmentViewSet
from scheduling.employee.views import EmployeeAppointmentViewSet
from scheduling.views import slot_list, EmployeeViewSet, CustomerViewSet

router = routers.DefaultRouter()
router.register(r'employees', EmployeeViewSet)
router.register(r'customers', CustomerViewSet)

router.register(r'customer/appointments', CustomerAppointmentViewSet, base_name='c-appointment')
router.register(r'employee/appointments', EmployeeAppointmentViewSet, base_name='e-appointment')


urlpatterns = [
    path("slots/", slot_list, name="slot-list"),
    path(r'', include(router.urls)),
    path(r'', include('rest_framework.urls', namespace='rest_framework')),
]