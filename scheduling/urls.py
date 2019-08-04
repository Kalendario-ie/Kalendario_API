from django.urls import include, path
from rest_framework import routers
from scheduling.views import *
from scheduling.models import Appointment

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'employees', EmployeeViewSet)
router.register(r'appointments', AppointmentViewSet, base_name=Appointment)


urlpatterns = [
    path("slots", slot_list, name="slot_list"),
    path(r'', include(router.urls)),
    path(r'', include('rest_framework.urls', namespace='rest_framework')),
]