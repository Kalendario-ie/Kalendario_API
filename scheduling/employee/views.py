from rest_framework.permissions import IsAuthenticated

from scheduling.employee.serializers import EmployeeAppointmentWriteSerializer
from scheduling.permissions import IsEmployee
from scheduling.views import AppointmentViewSet


class EmployeeAppointmentViewSet(AppointmentViewSet):
    permission_classes = (IsAuthenticated, IsEmployee)

    def custom_queryset_filter(self, queryset):
        return queryset.filter(employee_id=self.request.user.employee.id)

    def get_serializer_class(self):
        self.request.data['employee'] = self.request.user.employee.id
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update':
            return EmployeeAppointmentWriteSerializer
        return super().get_serializer_class()
