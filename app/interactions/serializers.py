from rest_framework import serializers

from activities.models import Activity
from activities.serializers import ActivitySerializer

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
        fields = ("pk", "activity", "activity_pk", "user", "type", "created_at")
        read_only_fields = ("pk", "created_at")

    serializer_choice_field = ChoiceDisplayField

    activity_pk = serializers.PrimaryKeyRelatedField(
        queryset=Activity.objects.all(),
        source="activity",
    )
    activity = ActivitySerializer(read_only=True, required=False)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
