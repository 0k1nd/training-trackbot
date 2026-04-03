from apps.accounts.models.users import User
from apps.core.models import TimeStampedModel
from django.db import models


class BodyMetrics(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bodymetrics")
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    body_fat_percent = models.PositiveIntegerField(blank=True, null=True)

    neck_cm = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    chest_cm = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    waist_cm = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    hips_cm = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    thigh_cm = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    calf_cm = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    biceps_cm = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    note = models.TextField(blank=True)

    class Meta:
        verbose_name = "body metric"
        verbose_name_plural = "body metrics"
        ordering = ["-created_at"]
