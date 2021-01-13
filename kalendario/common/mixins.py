from drf_rw_serializers import viewsets as drf

from kalendario.common.pagination import StandardResultsSetPagination

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from . import filters, permissions
from djangorestframework_camel_case.util import underscoreize


class RenderParserPaginationMixin:
    pagination_class = StandardResultsSetPagination


class AuthOwnerFilterMixin:
    authentication_classes = (TokenAuthentication,)
    filter_backends = [filters.OwnerFilter]

    def get_write_serializer(self, *args, **kwargs):
        serializer_class = self.get_write_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        # Ensures that the 'owner' field is present and it is the same as the user's company id
        # The filter by owner_id in queryset should make sure that this part will not be reached
        # if the user's owner_id does not match with the model owner_id
        kwargs['data'].update({'owner': self.request.user.owner_id})
        return serializer_class(*args, **kwargs)


class WithPermissionsMixin:
    def get_permissions(self):
        permission_classes = [IsAuthenticated, permissions.ModelPermission]
        return [perm() for perm in permission_classes]


class QuerysetSerializerMixin:
    queryset_serializer_class = None

    def get_queryset_serializer_class(self):
        return self.queryset_serializer_class

    def get_queryset_serializer(self, *args, **kwargs):
        serializer_class = self.get_queryset_serializer_class()
        return serializer_class(*args, **kwargs)

    def get_queryset_params(self):
        data = underscoreize(self.request.query_params)
        serializer = self.get_queryset_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data


class UpdateModelMixin(drf.UpdateModelMixin):
    pass


class RetrieveModelMixin(drf.RetrieveModelMixin):
    pass