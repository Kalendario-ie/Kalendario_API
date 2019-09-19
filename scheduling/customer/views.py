# from rest_framework import status
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
#
# from scheduling.serializers import CustomerAppointmentWriteSerializer
# from scheduling.permissions import IsCustomer
# from scheduling.views import AppointmentViewSet
#
#
# class CustomerAppointmentViewSet(AppointmentViewSet):
#     permission_classes = (IsAuthenticated, IsCustomer)
#
#     def get_queryset(self):
#         return super().get_queryset().filter(customer_id=self.request.user.person.id)
#
#     def get_serializer_class(self):
#         if self.action == 'create' or self.action == 'update' or self.action == 'partial_update':
#             return CustomerAppointmentWriteSerializer
#         return super().get_serializer_class()
#
#     def create(self, request, *args, **kwargs):
#         if 'customer' in self.request.data and self.request.data['customer'] != self.request.user.person.id:
#             return Response(status=status.HTTP_401_UNAUTHORIZED)
#         return super().create(request, args, kwargs)
