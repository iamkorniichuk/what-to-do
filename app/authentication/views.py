from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView

from .serializers import SignUpSerializer


User = get_user_model()


class SignUpView(CreateAPIView):
    serializer_class = SignUpSerializer
    queryset = User.objects.all()
    permission_classes = ()
