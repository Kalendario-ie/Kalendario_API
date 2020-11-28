from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from appointment_manager.common import mixins
from customers.models import get_availability_for_service
from customers import serializers

from scheduling import models

from appointment_manager.common import viewsets


class RequestViewSet(mixins.QuerysetSerializerMixin, viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    read_serializer_class = serializers.RequestReadSerializer

    def get_queryset_serializer_class(self):
        if self.action in ['current']:
            return serializers.RequestQueryRequiredOwnerSerializer
        return serializers.RequestQuerySerializer

    def get_write_serializer_class(self):
        if self.action == 'create':
            return serializers.AddAppointmentSerializer
        return serializers.RequestWriteSerializer

    def get_serializer_context(self):
        return {'user': self.request.user}

    @action(detail=False, methods=['get'])
    def current(self, request, *args, **kwargs):
        instance = self.get_current()
        serializer = self.get_read_serializer(instance)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        appointment_id = self.get_queryset_params().get('appointment')
        appointment = get_object_or_404(instance.appointment_set.all(), pk=appointment_id)
        appointment.delete()
        serializer = self.get_read_serializer(instance)
        return Response(serializer.data)

    def get_current(self):
        owner_id = self.get_queryset_params().get('owner')
        return models.Request.objects.get_current(owner_id, self.request.user.id)

    def get_queryset(self, **kwargs):
        queryset = models.Request.objects.filter(user_id=self.request.user.id).order_by('scheduled_date')
        params = self.get_queryset_params()

        from_date = params.get('from_date')
        if from_date is not None:
            queryset = queryset.filter(scheduled_date__gte=from_date)

        to_date = params.get('to_date')
        if to_date is not None:
            queryset = queryset.filter(scheduled_date__lte=to_date)

        return queryset

    @action(detail=True, methods=['post'])
    def payment(self, *args, **kwargs):
        request = self.get_object()
        intent = request.stripe_client_secret()
        return Response({'clientSecret': intent})


class CompanyViewSet(viewsets.ReadOnlyModelViewSet):

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.CompanyDetailsSerializer
        if self.action == 'slots':
            return serializers.EmployeeSerializer
        return serializers.CompanySerializer

    def retrieve(self, request, pk=None, *args, **kwargs):
        if not pk.isnumeric():
            self.lookup_field = 'name'
            self.kwargs.update({'name': pk})
        return viewsets.ReadOnlyModelViewSet.retrieve(self, request, *args, **kwargs)

    def get_queryset(self):
        if self.action == 'slots':
            return models.Employee.objects.all()

        queryset = models.Company.objects.get_public()
        params = self.request.query_params
        name = params.get('name')
        if name is not None:
            queryset = queryset.filter(name=name)

        search = self.request.query_params.get('search')
        if search is not None:
            queryset = queryset.filter(name__icontains=search)

        return queryset

    @action(detail=False, methods=['get'])
    def slots(self, request):
        data = request.query_params.copy()
        if hasattr(self.request.user, 'person_id'):
            data['customer'] = self.request.user.person_id
        query_serializer = serializers.SlotQuerySerializer(data=data)
        query_serializer.is_valid(raise_exception=True)
        slots = get_availability_for_service(**query_serializer.validated_data)
        slot_serializer = serializers.SlotSerializer(slots, many=True)
        return Response(slot_serializer.data)
