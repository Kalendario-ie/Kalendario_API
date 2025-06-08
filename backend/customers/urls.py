from django.urls import include, path
from rest_framework import routers
from customers import views

router = routers.DefaultRouter()
router.register(r'companies', views.CompanyViewSet, 'customer-company')
router.register(r'requests', views.RequestViewSet, 'customer-request')
router.register(r'appointments', views.AppointmentViewSet, 'customer-appointments')

urlpatterns = [
    path(r'', include(router.urls)),
]
