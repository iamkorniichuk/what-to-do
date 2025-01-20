from rest_framework import serializers

from users.serializers import UserSerializer

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
        )
        read_only_fields = ("pk", "created_by")

    media = ActivityMediaSerializer(many=True, read_only=True)
    files = serializers.ListField(child=serializers.FileField(), write_only=True)
    created_by = UserSerializer(read_only=True, required=False)
    created_by_pk = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
        source="created_by",
    )

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
