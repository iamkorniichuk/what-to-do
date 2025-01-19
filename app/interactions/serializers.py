from rest_framework import serializers

from activities.models import Activity
from activities.serializers import ActivitySerializer
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
            "user",
            "user_pk",
            "type",
            "created_at",
        )
        read_only_fields = ("pk", "created_at", "user")

    serializer_choice_field = ChoiceDisplayField

    activity = ActivitySerializer(read_only=True, required=False)
    activity_pk = serializers.PrimaryKeyRelatedField(
        queryset=Activity.objects.all(),
        source="activity",
    )
    user = UserSerializer(read_only=True, required=False)
    user_pk = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
        source="user",
    )
