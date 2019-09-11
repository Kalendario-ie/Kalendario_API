from rest_framework.permissions import IsAuthenticated

from scheduling.employee.serializers import EmployeeAppointmentWriteSerializer
from scheduling.permissions import IsEmployee
from scheduling.views import AppointmentViewSet


class EmployeeAppointmentViewSet(AppointmentViewSet):
    permission_classes = (IsAuthenticated, IsEmployee)

    def custom_queryset_filter(self, queryset):
        if self.request.user.has_perm('scheduling.view_appointment'):
            return queryset
        return queryset.filter(employee_id=self.request.user.employee.id)

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update':
            return EmployeeAppointmentWriteSerializer
        return super().get_serializer_class()

    def request_data(self):
        request = self.request.data.copy()
        if not self.request.user.has_perm('scheduling.change_appointment'):
            request['employee'] = self.request.user.employee.id
        return request
