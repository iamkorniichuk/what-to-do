from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer

from users.serializers import UserSerializer

from .models import Schedule, WorkDay, TimeRange


class TimeRangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeRange
        fields = ("pk", "start", "end")
        read_only_fields = ("pk",)


class WorkDaySerializer(WritableNestedModelSerializer):
    class Meta:
        model = WorkDay
        fields = ("pk", "day", "work_hours", "break_hours")
        read_only_fields = ("pk",)

    work_hours = TimeRangeSerializer()
    break_hours = TimeRangeSerializer(many=True, allow_null=True)


class ScheduleSerializer(WritableNestedModelSerializer):
    class Meta:
        model = Schedule
        fields = (
            "pk",
            "work_days",
            "created_by",
            "created_by_pk",
        )
        read_only_fields = ("pk",)

    work_days = WorkDaySerializer(many=True)
    created_by = UserSerializer(read_only=True, required=False)
    created_by_pk = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
        source="created_by",
    )
