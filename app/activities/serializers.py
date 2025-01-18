from rest_framework import serializers

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
            "user",
            "media",
            "files",
        )
        read_only_fields = ("pk",)

    media = ActivityMediaSerializer(many=True, read_only=True)
    files = serializers.ListField(child=serializers.FileField(), write_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

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
        for order, file in enumerate(files):
            ActivityMedia.objects.create(
                activity=activity,
                order=order,
                file=file,
            )
        return activity
