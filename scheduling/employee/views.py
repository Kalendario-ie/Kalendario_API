# from rest_framework import status
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
#
# from scheduling.serializers import EmployeeAppointmentWriteSerializer
# from scheduling.permissions import IsEmployee
# from scheduling.views import AppointmentViewSet
#
#
# class EmployeeAppointmentViewSet(AppointmentViewSet):
#     permission_classes = (IsAuthenticated, IsEmployee)
#
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         if self.request.user.has_perm('scheduling.view_appointment'):
#             return queryset
#         return queryset.filter(employee_id=self.request.user.person.id)
#
#     def get_serializer_class(self):
#         if self.action == 'create' or self.action == 'update' or self.action == 'partial_update':
#             return EmployeeAppointmentWriteSerializer
#         return super().get_serializer_class()
#
#     def create(self, request, *args, **kwargs):
#         if self.request.user.has_perm('scheduling.change_appointment'):
#             return super().create(request, args, kwargs)
#         if 'employee' in self.request.data and self.request.data['employee'] != self.request.user.person.id:
#             return Response(status=status.HTTP_401_UNAUTHORIZED)
#         return super().create(request, args, kwargs)
