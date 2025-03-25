from django.contrib.postgres.search import TrigramSimilarity
from rest_framework.generics import ListAPIView

from .serializers import AutocompleteTerritorySerializer, TerritorySerializer, Territory


class TerritoryAutocompleteView(ListAPIView):
    queryset = Territory.objects.all()
    serializer_class = TerritorySerializer

    def filter_queryset(self, queryset):
        queries = self.request.query_params
        serializer = AutocompleteTerritorySerializer(data=queries)
        serializer.is_valid(raise_exception=True)

        name = serializer.data["name"]

        queryset = self.get_queryset().annotate(
            similarity=TrigramSimilarity("name", name)
        )

        return queryset.filter(similarity__gte=0.3).order_by("-similarity").all()
