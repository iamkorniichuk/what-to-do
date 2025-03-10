from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class TimeRange(models.Model):
    start = models.TimeField()
    end = models.TimeField()

    def __str__(self):
        return f"{self.start} - {self.end}"


class WorkDay(models.Model):
    class WeekDayChoices(models.IntegerChoices):
        MONDAY = 1, "monday"
        TUESDAY = 2, "tuesday"
        WEDNESDAY = 3, "wednesday"
        THURSDAY = 4, "thursday"
        FRIDAY = 5, "friday"
        SATURDAY = 6, "saturday"
        SUNDAY = 7, "sunday"

    day = models.PositiveSmallIntegerField(choices=WeekDayChoices.choices)
    work_hours = models.ForeignKey(
        TimeRange,
        models.CASCADE,
        related_name="works",
    )
    break_hours = models.ManyToManyField(
        TimeRange,
        blank=True,
        related_name="breaks",
    )

    def __str__(self):
        return f"{self.pk} {self.get_day_display()}"


class Schedule(models.Model):
    work_days = models.ManyToManyField(
        WorkDay,
        related_name="schedules",
    )
    created_by = models.ForeignKey(User, models.CASCADE)

    def __str__(self):
        return str(self.pk)
