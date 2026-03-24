from django.db import models

from apps.core.models import TimeStampedModel
from apps.accounts.models import User
from apps.trainings.models import Exercise
from apps.core import constants

class Workout(TimeStampedModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='workouts'
    )
    note = models.TextField(
        blank=True,
        null=True
    )
    workout_type = models.CharField(
        max_length=20,
        choices=constants.WorkoutType.choices,
        default=constants.WorkoutType.FULL_BODY
    )

    class Meta:
        ordering = ["-created_at"]


class WorkoutExercise(models.Model):
    workout = models.ForeignKey(
        Workout,
        on_delete=models.CASCADE,
        related_name="items"
    )
    exercise = models.ForeignKey(
        Exercise,
        on_delete=models.PROTECT,
        related_name="workout_exercises",
    )
    order = models.PositiveIntegerField(default=1)
    note = models.TextField(
        null=True,
        blank=True
    )