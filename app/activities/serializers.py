from rest_framework import serializers

from .models import Activity


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = (
            "name",
            "description",
            "user",
            "interaction",
        )

    interaction = serializers.SerializerMethodField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def get_interaction(self, activity):
        current_user = self.context["request"].user
        interaction = activity.interactions.filter(user=current_user).first()
        if interaction:
            return interaction.get_type_display()
        return None
