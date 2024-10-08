from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)

from .serializers import SignUpSerializer, LoginSerializer, LoginRefreshSerializer


User = get_user_model()


class SignUpView(CreateAPIView):
    serializer_class = SignUpSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)


class LoginRefreshView(TokenRefreshView):
    serializer_class = LoginRefreshSerializer
    permission_classes = [AllowAny]


class LogoutView(TokenBlacklistView):
    permission_classes = [AllowAny]
