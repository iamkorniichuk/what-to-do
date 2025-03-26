from django.db.models import Count, Q
from rest_framework.generics import ListAPIView

from activities.serializers import ActivitySerializer, Activity
from interactions.models import Interaction


class RecommendationView(ListAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

    limit = 40

    def filter_queryset(self, queryset):
        current_user = self.request.user
        user_embedding = Interaction.objects.get_user_embedding(current_user)

        if user_embedding is None:
            queryset = queryset.annotate(
                likes=Count("interactions", filter=Q(interactions__type=self.like_type))
            ).order_by("-likes")
        else:
            queryset = queryset.order_by_embedding_distance(user_embedding)

        return queryset[: self.limit]
