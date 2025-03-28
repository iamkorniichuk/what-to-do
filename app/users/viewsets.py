from rest_framework import viewsets, mixins, parsers
from rest_framework.decorators import action

from .serializers import User, UserSerializer


class UserViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    @action(methods=["get", "put", "patch"], detail=False)
    def my(self, request):
        current_user = request.user
        self.kwargs["pk"] = current_user.pk

        if request.method == "GET":
            return self.retrieve(request, *self.args, **self.kwargs)
        elif request.method in ["PUT", "PATCH"]:
            return self.update(request, *self.args, **self.kwargs)
