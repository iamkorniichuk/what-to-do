from django.core.validators import EMPTY_VALUES
from django.contrib.postgres.search import SearchVector
from django_filters import rest_framework as filters

from .models import Activity


class SearchFilter(filters.CharFilter):
    def __init__(self, fields, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.search_fields = fields

    def filter(self, qs, value):
        if value in EMPTY_VALUES:
            return qs

        qs = qs.annotate(search=SearchVector(*self.search_fields))
        return qs.filter(search=value)


class ActivityFilterSet(filters.FilterSet):
    class Meta:
        model = Activity
        fields = ("name", "is_remote")

    is_remote = filters.BooleanFilter(
        field_name="location",
        lookup_expr="isnull",
    )
    duration__gte = filters.DurationFilter(
        field_name="duration",
        lookup_expr="gte",
    )
    duration__lte = filters.DurationFilter(
        field_name="duration",
        lookup_expr="lte",
    )
    search = SearchFilter(
        fields=(
            "name",
            "description",
            "created_by__username",
            "created_by__description",
        )
    )
