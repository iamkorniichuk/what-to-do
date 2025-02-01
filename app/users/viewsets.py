from rest_framework import viewsets, mixins, parsers
from rest_framework.decorators import action

from .models import User
from .serializers import UserSerializer


class UserViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    @action(methods=["get", "put", "patch"], detail=False)
    def my(self, request):
        current_user = self.request.user
        self.kwargs["pk"] = current_user.pk

        if request.method == "GET":
            return self.retrieve(request, *self.args, **self.kwargs)
        elif request.method in ["PUT", "PATCH"]:
            return self.update(request, *self.args, **self.kwargs)
