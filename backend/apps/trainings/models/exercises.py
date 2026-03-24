from django.db import models

from apps.accounts.models import User
from apps.core import constants


class Exercise(models.Model):
    name = models.CharField(
        max_length=100,
    )
    description = models.TextField(
        blank=True,
        null=True
    )
    primary_muscle = models.CharField(
        max_length=24,
        choices=constants.MuscleGroup.choices,
    )
    secondary_muscle = models.CharField(
        max_length=24,
        choices=constants.MuscleGroup.choices,
        blank=True,
        null=True
    )
    equipment = models.CharField(
        max_length=24,
        choices=constants.EquipmentType.choices,
        default=constants.EquipmentType.BODYWEIGHT,
    )
    is_basic = models.BooleanField(
        default=True
    )
    author = models.ForeignKey(
        User,
        related_name='exercise',
        on_delete=models.CASCADE,
        editable=False
    )
    

    def __str__(self):
        return self.name