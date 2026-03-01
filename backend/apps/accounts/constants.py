from django.db import models

class GenderType(models.TextChoices):
    MAN = "M", "man"
    WOMAN = "W", "woman"