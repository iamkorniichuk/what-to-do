from rest_framework import serializers

from users.serializers import UserSerializer
from schedules.serializers import Schedule, ScheduleSerializer

from .models import Activity, RecurringActivity, ActivityMedia, ActivityTypeChoices


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
            "type",
            "type_label",
            "media",
            "files",
            "location",
            "duration",
            "is_remote",
        )
        read_only_fields = (
            "pk",
            "created_by",
            "type",
            "type_label",
        )

    media = ActivityMediaSerializer(many=True, read_only=True)
    files = serializers.ListField(child=serializers.FileField(), write_only=True)
    created_by = UserSerializer(read_only=True, required=False)
    created_by_pk = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
        source="created_by",
    )
    is_remote = serializers.SerializerMethodField()
    type_label = serializers.SerializerMethodField()

    def get_is_remote(self, obj):
        return obj.location is None

    def get_type_label(self, obj):
        return obj.get_type_display()

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


class RecurringActivitySerializer(ActivitySerializer):
    class Meta:
        model = RecurringActivity
        fields = ActivitySerializer.Meta.fields + (
            "schedule",
            "schedule_pk",
        )

    schedule = ScheduleSerializer(read_only=True, required=False)
    schedule_pk = serializers.PrimaryKeyRelatedField(
        queryset=Schedule.objects.all(),
        source="schedule",
    )


class PolymorphicActivitySerializer(serializers.Serializer):
    @classmethod
    def get_serializer_class(cls, type_value):
        if type_value == ActivityTypeChoices.RECURRING:
            return RecurringActivitySerializer

    def to_representation(self, instance):
        if isinstance(instance, RecurringActivity):
            serializer = RecurringActivitySerializer(instance, context=self.context)
        return serializer.data

    def to_internal_value(self, data):
        activity_type = data["type"]
        serializer_class = self.get_serializer_class(activity_type)
        serializer = serializer_class(data=data, context=self.context)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data

    def create(self, data):
        activity_type = data["type"]
        serializer_class = self.get_serializer_class(activity_type)
        serializer = serializer_class()
        instance = serializer.create(data)
        return instance

    def update(self, instance, data):
        serializer_class = self.get_serializer_class(data.get("type", instance.type))
        serializer = serializer_class(
            instance=instance,
            data=data,
            partial=self.partial,
            context=self.context,
        )
        return serializer.save()
