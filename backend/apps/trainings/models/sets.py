from apps.core import constants
from apps.core.models import TimeStampedModel
from apps.trainings.models import WorkoutExercise
from django.db import models


class Set(TimeStampedModel):
    workout_exercise = models.ForeignKey(
        WorkoutExercise, on_delete=models.CASCADE, related_name="sets"
    )
    set_number = models.PositiveIntegerField()
    weight = models.FloatField(null=True, blank=True)
    reps = models.PositiveIntegerField(null=True, blank=True)

    difficulty = models.CharField(
        max_length=20, choices=constants.Difficulty.choices, default=constants.Difficulty.MODERATE
    )

    class Meta:
        ordering = ["-created_at"]
