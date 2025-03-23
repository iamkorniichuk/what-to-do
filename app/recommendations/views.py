from django.db.models import Avg, F, Value, When, Case, Count, Q
from django.db.models.functions import Coalesce
from rest_framework.views import APIView
from rest_framework.response import Response

from pgvector.django import L2Distance

from activities.models import Activity
from activities.serializers import ActivitySerializer
from interactions.models import Interaction


class RecommendationsView(APIView):
    like_type = Interaction.TypeChoices.LIKE
    dislike_type = Interaction.TypeChoices.DISLIKE
    like_weight = 1.0
    dislike_weight = 0.5
    limit = 40

    def calculate_user_embedding(self, user):
        user_embedding = (
            Activity.objects.filter(interactions__created_by=user)
            .annotate(
                weighted_embedding=Case(
                    When(
                        interactions__type=self.like_type,
                        then=F("embedding") * self.like_weight,
                    ),
                    When(
                        interactions__type=self.dislike_type,
                        then=F("embedding") * -self.dislike_weight,
                    ),
                )
            )
            .aggregate(user_embedding=Coalesce(Avg("weighted_embedding"), Value(None)))[
                "user_embedding"
            ]
        )

        return user_embedding

    def get(self, request):
        current_user = request.user
        user_embedding = self.calculate_user_embedding(current_user)

        if user_embedding is None:
            activities = Activity.objects.annotate(
                likes=Count("interactions", filter=Q(interactions__type=self.like_type))
            ).order_by("-likes")[: self.limit]
        else:
            activities = Activity.objects.alias(
                distance=L2Distance("embedding", user_embedding)
            ).order_by("distance")[: self.limit]

        serializer = ActivitySerializer(activities, many=True)
        return Response(serializer.data)
