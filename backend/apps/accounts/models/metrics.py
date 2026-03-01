from django.db import models

from apps.accounts.models import User


class BodyMetrics(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    date = models.DateTimeField(
        auto_now_add=True
    )
    weight_kg = models.PositiveIntegerField()
    body_fat_percent = models.PositiveIntegerField(
        blank=True,
        null=True
    )

    neck_cm = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    chest_cm = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    waist_cm = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    hips_cm = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    thigh_cm = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    calf_cm = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    biceps_cm = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    note = models.TextField(
        blank=True
    )


    class Meta:
        verbose_name = "body metric"
        verbose_name_plural = "body metrics"
        ordering = ["-date"]
