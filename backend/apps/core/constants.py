from django.db import models


class GenderType(models.TextChoices):
    MAN = "M", "man"
    WOMAN = "W", "woman"


class MuscleGroup(models.TextChoices):
    CHEST = "chest", "Грудь"
    BACK = "back", "Спина"
    SHOULDERS = "shoulders", "Плечи"
    BICEPS = "biceps", "Бицепс"
    TRICEPS = "triceps", "Трицепс"
    LEGS = "legs", "Ноги (квадрицепс)"
    GLUTES = "glutes", "Ягодицы"
    CALVES = "calves", "Икры"
    CORE = "core", "Пресс/кор"


class EquipmentType(models.TextChoices):
    BODYWEIGHT = "bodyweight", "Собственный вес"
    DUMBBELL = "dumbbell", "Гантели"
    BARBELL = "barbell", "Штанга"
    MACHINE = "machine", "Тренажёр"
    KETTLEBELL = "kettlebell", "Гиря"
    CABLE = "cable", "Блочный тренажёр"
    OTHER = "other", "Другое"


class WorkoutType(models.TextChoices):
    STRENGTH = "strength", "Сила (низкие повторы, большой вес)"
    HYPERTROPHY = "hypertrophy", "Масса (8–15 повторений)"
    ENDURANCE = "endurance", "Выносливость (высокие повторения)"
    POWER = "power", "Мощность (взрывные движения)"
    FULL_BODY = "full_body", "Фуллбоди"
    UPPER = "upper", "Верх"
    LOWER = "lower", "Низ"
    PUSH = "push", "Жим (push)"
    PULL = "pull", "Тяга (pull)"
    CARDIO = "cardio", "Кардио"
    MOBILITY = "mobility", "Мобилити/растяжка"
    DELOAD = "deload", "Делоад/лёгкая"


class Difficulty(models.TextChoices):
    EASY = "easy", "Легко"
    MODERATE = "moderate", "Средне"
    HARD = "hard", "Тяжело"
