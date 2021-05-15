from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from kalendario.common import mixins, mail, viewsets
from customers.models import get_availability_for_service
from customers import serializers
from scheduling import models

import logging
logger = logging.getLogger(__name__)


class RequestViewSet(mixins.QuerysetSerializerMixin,
                     mixins.RequireAuthMixin,
                     mixins.UpdateModelMixin,
                     viewsets.ReadOnlyModelViewSet):
    read_serializer_class = serializers.RequestReadSerializer
    write_serializer_class = serializers.RequestWriteSerializer

    def get_queryset_serializer_class(self):
        if self.action in ['current']:
            return serializers.RequestQueryRequiredOwnerSerializer
        return serializers.RequestQuerySerializer

    def get_serializer_context(self):
        return {'user': self.request.user}

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

    def get_current(self, owner_id=None):
        if not owner_id:
            owner_id = self.get_queryset_params().get('owner')
        instance = models.Request.objects.get_current(owner_id, self.request.user.id)
        serializer = self.get_read_serializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def current(self, request, *args, **kwargs):
        return self.get_current()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        appointment_id = self.get_queryset_params().get('appointment')
        appointment = get_object_or_404(instance.appointment_set.all(), pk=appointment_id)
        appointment.delete()
        serializer = self.get_read_serializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def add(self, request, *args, **kwargs):
        serializer = serializers.AddAppointmentSerializer(data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        serializer.save()
        read_serializer = self.get_read_serializer(serializer.instance)
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def delete(self, request, *args, **kwargs):
        """
        This is different from destroy as this method allows to delete the appointment by only providing the id of the appointment
        :param request: params {appointment: number}
        """
        appointment_id = self.request.data['appointment']
        appointment = models.Appointment.objects.get(pk=appointment_id)
        if appointment and appointment.customer.user_id == request.user.id:
            owner_id = appointment.owner_id
            appointment.delete()
            return self.get_current(owner_id)
        return Response({'error': 'invalid appointment id'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    @action(detail=True, methods=['patch'])
    def confirm(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = serializers.RequestWriteSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(complete=True)
        message = instance.owner.config.post_book_email_message
        try:
            mail.send_mail('Request Submitted', message, [request.user.email])
        except Exception as e:
            logger.error(f'could not email user {request.user.email}: {e}')
        read_serializer = self.get_read_serializer(instance)
        return Response(read_serializer.data, status=status.HTTP_200_OK)


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
