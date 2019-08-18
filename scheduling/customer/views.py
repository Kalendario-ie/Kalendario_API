from rest_framework.permissions import IsAuthenticated

from scheduling.permissions import IsCustomer
from scheduling.views import AppointmentViewSet


class CustomerAppointmentViewSet(AppointmentViewSet):
    permission_classes = (IsAuthenticated, IsCustomer)

    def custom_queryset_filter(self, queryset):
        return queryset.filter(customer_id=self.request.user.id)

    def get_serializer_class(self):
        self.request.data['customer'] = self.request.user.id
        return super().get_serializer_class()