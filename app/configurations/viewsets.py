from rest_framework import viewsets, mixins
from rest_framework.decorators import action

from .models import Configuration
from .serializers import ConfigurationSerializer


class ConfigurationViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Configuration.objects.all()
    serializer_class = ConfigurationSerializer

    @action(methods=["get", "put", "patch"], detail=False)
    def my(self, request):
        current_user_configuration = request.user.configuration
        self.kwargs["pk"] = current_user_configuration.pk

        if request.method == "GET":
            return self.retrieve(request, *self.args, **self.kwargs)
        elif request.method in ["PUT", "PATCH"]:
            return self.update(request, *self.args, **self.kwargs)
