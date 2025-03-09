from rest_framework import serializers

from users.serializers import UserSerializer
from schedules.models import Schedule
from schedules.serializers import ScheduleSerializer

from .models import Activity, ActivityMedia


class ActivityMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityMedia
        fields = (
            "pk",
            "file",
            "order",
            "created_at",
        )
        read_only_fields = ("pk", "order", "created_at")


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = (
            "pk",
            "name",
            "description",
            "created_by",
            "created_by_pk",
            "media",
            "files",
            "location",
            "schedule",
            "schedule_pk",
            "duration",
            "is_remote",
        )
        read_only_fields = ("pk", "created_by", "schedule")

    media = ActivityMediaSerializer(many=True, read_only=True)
    files = serializers.ListField(child=serializers.FileField(), write_only=True)
    created_by = UserSerializer(read_only=True, required=False)
    created_by_pk = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
        source="created_by",
    )
    schedule = ScheduleSerializer(read_only=True, required=False)
    schedule_pk = serializers.PrimaryKeyRelatedField(
        queryset=Schedule.objects.all(),
        source="schedule",
    )
    is_remote = serializers.SerializerMethodField()

    def get_is_remote(self, obj):
        return obj.location is None

    def validate_files(self, files):
        for file in files:
            serializer = ActivityMediaSerializer(data={"file": file})
            serializer.is_valid(raise_exception=True)

        max_length = 10
        if len(files) > max_length:
            raise serializers.ValidationError(
                f"You can upload up to {max_length} media files only."
            )
        return files

    def create(self, validated_data):
        files = validated_data.pop("files")

        activity = Activity.objects.create(**validated_data)

        media = []
        for order, file in enumerate(files):
            obj = ActivityMedia(
                activity=activity,
                order=order,
                file=file,
            )
            media.append(obj)

        ActivityMedia.objects.bulk_create(media)
        return activity
