from django.contrib.auth import get_user_model
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from .serializers import UserSerializer


class RegisterViewSet(CreateModelMixin, GenericViewSet):
    permission_classes = [AllowAny]
    model = get_user_model()
    serializer_class = UserSerializer


class AuthenticatedUserView(APIView):
    def get(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
