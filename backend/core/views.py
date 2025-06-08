from rest_framework.decorators import action
from rest_framework.response import Response

from kalendario.common import mixins, viewsets
from core import models, serializers


class UserViewSet(mixins.WithPermissionsMixin,
                  mixins.AuthOwnerFilterMixin,
                  viewsets.ModelViewSet):
    read_serializer_class = serializers.UserAdminReadSerializer
    write_serializer_class = serializers.UserAdminWriteSerializer
    queryset = models.User.objects.all()

    @action(detail=True, methods=['patch'])
    def changePassword(self, request, *args, **kwargs):
        instance = self.get_object()

        # Change Password
        context = {'request': self.request}
        serializer = serializers.PasswordChangeSerializer(instance, data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Return User
        serializer = self.get_read_serializer(instance)
        return Response(serializer.data)


class GroupProfileViewSet(mixins.WithPermissionsMixin,
                          mixins.AuthOwnerFilterMixin,
                          viewsets.ModelViewSet):
    serializer_class = serializers.GroupProfileSerializer
    queryset = models.GroupProfile.objects.all()

    @action(detail=False, methods=['get'])
    def permissions(self, request, *args, **kwargs):
        queryset = models.permissions()
        serializer = serializers.PermissionsSerializer(queryset, many=True)
        return Response(serializer.data)
