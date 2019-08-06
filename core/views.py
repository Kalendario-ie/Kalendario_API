from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import  authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import User
from core.serializers import UserSerializer


@authentication_classes([TokenAuthentication, SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
class CurrentUserView(APIView):
    def get(self, request):
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
