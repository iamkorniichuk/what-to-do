from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .serializers import SignUpSerializer


User = get_user_model()


class SignUpView(CreateAPIView, TokenObtainPairView):
    queryset = User.objects.all()
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        self.serializer_class = SignUpSerializer
        super(CreateAPIView, self).create(request, *args, **kwargs)

        self.serializer_class = TokenObtainPairSerializer
        return super(TokenObtainPairView, self).post(request, *args, **kwargs)
