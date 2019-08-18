from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import User
from core.serializers import UserSerializer


class UserViewSet(viewsets.GenericViewSet):
    authentication_classes = (TokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()

    serializer_class = UserSerializer

    @action(detail=False, methods=['get'])
    def current(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class ObtainAuthUserView(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        token = super(ObtainAuthUserView, self).post(request, args, kwargs)
        user_email = request.data['username']
        user = User.objects.filter(email=user_email).first()
        serializer = UserSerializer(user)
        token.data['user'] = serializer.data

        return token
