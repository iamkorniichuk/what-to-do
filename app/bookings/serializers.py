from rest_framework import serializers

from activities.serializers import ActivitySerializer, Activity
from users.serializers import UserSerializer

from .models import Booking


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = (
            "pk",
            "appointment_datetime",
            "activity",
            "activity_pk",
            "booked_by",
            "booked_by_pk",
        )
        read_only_fields = (
            "pk",
            "activity",
            "booked_by",
        )

    activity = ActivitySerializer(required=False)
    activity_pk = serializers.PrimaryKeyRelatedField(
        queryset=Activity.objects.all(),
        source="activity",
    )
    booked_by = UserSerializer(required=False)
    booked_by_pk = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
        source="booked_by",
    )
