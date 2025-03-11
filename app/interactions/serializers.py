from rest_framework import serializers

from activities.serializers import Activity, ActivitySerializer
from users.serializers import UserSerializer

from .models import Interaction


class ChoiceDisplayField(serializers.ChoiceField):
    def to_representation(self, obj):
        if obj and self.allow_blank:
            return obj

        return self._choices[obj]

    def to_internal_value(self, data):
        if data == "" and self.allow_blank:
            return ""

        for key, value in self._choices.items():
            if value == data:
                return key

        self.fail("invalid_choice", input=data)


class InteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interaction
        fields = (
            "pk",
            "activity",
            "activity_pk",
            "created_by",
            "created_by_pk",
            "type",
            "created_at",
        )
        read_only_fields = ("pk", "activity", "created_by", "created_at")
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Interaction.objects.all(),
                fields=["activity", "created_by_pk"],
            )
        ]

    serializer_choice_field = ChoiceDisplayField

    activity = ActivitySerializer(required=False)
    activity_pk = serializers.PrimaryKeyRelatedField(
        queryset=Activity.objects.all(),
        source="activity",
    )
    created_by = UserSerializer(required=False)
    created_by_pk = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
        source="created_by",
    )
