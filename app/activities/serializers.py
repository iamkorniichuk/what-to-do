from rest_framework import serializers

from .models import Activity


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = (
            "name",
            "description",
            "user",
            "get_interaction",
        )

    def get_interaction(self, activity):
        user = self.context["current_user"]
        interaction = activity.interactions.filter(user=user).first()
        if interaction:
            return interaction.get_type_display()
        return None
