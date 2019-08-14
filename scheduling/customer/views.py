from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from scheduling.customer.serializers import *
from scheduling.models import *
from scheduling.serializers import AppointmentReadSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class AppointmentViewSet(mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         viewsets.GenericViewSet):

    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return AppointmentReadSerializer
        self.request.data['customer'] = self.request.user.id
        return AppointmentWriteSerializer

    def get_queryset(self):
        queryset = Appointment.objects.all()

        queryset = queryset.filter(customer_id=self.request.user.id)

        employee = self.request.query_params.get('employee')
        if employee is not None:
            queryset = queryset.filter(employee=employee)

        from_date = self.request.query_params.get('from_date')
        if from_date is not None:
            queryset = queryset.filter(start__gte=from_date)

        to_date = self.request.query_params.get('to_date')
        if to_date is not None:
            queryset = queryset.filter(start__lte=to_date)

        return queryset


