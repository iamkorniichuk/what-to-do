from django.db.models import Q, F, ExpressionWrapper, DateTimeField
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

    def validate(self, fields):
        if not self.is_appointment_datetime_in_work_hours(fields):
            raise serializers.ValidationError(
                {
                    "appointment_datetime": "The appointment time is outside of working hours"
                }
            )

        if not self.is_appointment_datetime_free(fields):
            raise serializers.ValidationError(
                {"appointment_datetime": "The appointment time is already booked"}
            )

        return fields

    def is_appointment_datetime_in_work_hours(self, fields):
        activity = fields["activity"]
        schedule = activity.schedule
        appointment_start = fields["appointment_datetime"]

        weekday = appointment_start.weekday()
        time = appointment_start.time()

        is_in_work_hours = (
            schedule.work_days.filter(
                day=weekday,
                work_hours__start__lte=time,
                work_hours__end__gte=time,
            )
            .exclude(
                break_hours__start__lte=time,
                break_hours__end__gte=time,
            )
            .exists()
        )
        return is_in_work_hours

    def is_appointment_datetime_free(self, fields):
        booking_duration = fields["schedule"].booking_duration
        appointment_start = fields["appointment_datetime"]
        appointment_end = fields["appointment_datetime"] + booking_duration
        bookings = fields["activity"].bookings.annotate(
            appointment_datetime_end=ExpressionWrapper(
                F("appointment_datetime") + booking_duration,
                output_field=DateTimeField(),
            )
        )

        overlapping_bookings = bookings.filter(
            Q(
                appointment_datetime__lt=appointment_end,
                appointment_datetime__gte=appointment_start,
            )
            | Q(
                appointment_datetime__lte=appointment_start,
                appointment_datetime_end__gt=appointment_start,
            )
            | Q(
                appointment_datetime__gte=appointment_start,
                appointment_datetime__lt=appointment_end,
            )
            | Q(
                appointment_datetime__lt=appointment_start,
                appointment_datetime_end__gt=appointment_end,
            )
        )

        if self.instance:
            overlapping_bookings = overlapping_bookings.exclude(id=self.instance.id)

        return not overlapping_bookings.exists()
