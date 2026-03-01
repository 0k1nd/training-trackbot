from django.db import models
from django.contrib.auth.models import AbstractUser

from apps.accounts.constants import GenderType


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        blank=False,
        null=False
    )
    chat_id = models.BigIntegerField(
        blank=True,
        null=True,
        unique=True
    )
    gender = models.CharField(
        max_length=1,
        choices=GenderType,
        blank=True,
        null=True
    )
    was_born_at = models.DateField(
        blank=True,
        null=True
    )

    registed_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        verbose_name = ("user")
        verbose_name_plural = ("users")
        ordering = ["-registed_at"]