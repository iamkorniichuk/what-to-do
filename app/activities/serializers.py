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
            "interaction",
            "media",
            "files",
        )
        read_only_fields = ("pk",)

    media = ActivityMediaSerializer(many=True, read_only=True)
    files = serializers.ListField(child=serializers.FileField(), write_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    interaction = serializers.SerializerMethodField()

    def get_interaction(self, activity) -> str:
        current_user = self.context["request"].user
        interaction = activity.interactions.filter(user=current_user).first()
        if interaction:
            return interaction.get_type_display()
        return None

    def validate_files(self, value):
        max_length = 10

        if len(value) > max_length:
            raise serializers.ValidationError(
                f"You can upload up to {max_length} media files only."
            )
        return value

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
