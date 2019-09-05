from rest_framework.permissions import IsAuthenticated

from scheduling.customer.serializers import CustomerAppointmentWriteSerializer
from scheduling.permissions import IsCustomer
from scheduling.views import AppointmentViewSet


class CustomerAppointmentViewSet(AppointmentViewSet):
    permission_classes = (IsAuthenticated, IsCustomer)

    def custom_queryset_filter(self, queryset):
        return queryset.filter(customer_id=self.request.user.id)

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update':
            return CustomerAppointmentWriteSerializer
        return super().get_serializer_class()

    def request_data(self):
        request = self.request.data.copy()
        request['customer'] = self.request.user.id
        return request
