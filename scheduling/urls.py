from django.urls import include, path
from rest_framework import routers
import scheduling.customer.views as customer
from scheduling.views import slot_list, EmployeeViewSet

router = routers.DefaultRouter()
router.register(r'employees', EmployeeViewSet)
router.register(r'customer/appointments', customer.AppointmentViewSet, base_name='appointment')
router.register(r'customer/register', customer.CustomerViewSet)


urlpatterns = [
    path("slots/", slot_list, name="slot-list"),
    path(r'', include(router.urls)),
    path(r'', include('rest_framework.urls', namespace='rest_framework')),
]