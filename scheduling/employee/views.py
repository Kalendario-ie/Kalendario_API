from rest_framework.permissions import IsAuthenticated
from scheduling.permissions import IsEmployee
from scheduling.views import AppointmentViewSet


class EmployeeAppointmentViewSet(AppointmentViewSet):
    permission_classes = (IsAuthenticated, IsEmployee)

    def custom_queryset_filter(self, queryset):
        return queryset.filter(employee_id=self.request.user.employee.id)

    def get_serializer_class(self):
        self.request.data['employee'] = self.request.user.employee.id
        return super().get_serializer_class()