from django.urls import include, path
from rest_framework import routers
from scheduling.views import EmployeeViewSet, AppointmentViewSet, CompanyViewSet

router = routers.DefaultRouter()
router.register(r'employees', EmployeeViewSet, base_name='employee')
router.register(r'appointments', AppointmentViewSet, base_name='appointment')
router.register(r'companies', CompanyViewSet, base_name='company')

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'admin/', include('scheduling.api_admin.urls')),
    path(r'', include('rest_framework.urls', namespace='rest_framework'))
]
