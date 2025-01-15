from rest_framework import serializers

from .models import Activity


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = (
            "pk",
            "name",
            "description",
            "user",
            "interaction",
        )
        read_only_fields = ("pk",)

    interaction = serializers.SerializerMethodField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def get_interaction(self, activity) -> str:
        current_user = self.context["request"].user
        interaction = activity.interactions.filter(user=current_user).first()
        if interaction:
            return interaction.get_type_display()
        return None
