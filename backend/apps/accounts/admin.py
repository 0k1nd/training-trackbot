# apps/accounts/admin.py
from django.contrib import admin

from .models import User, BodyMetrics


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "was_born_at",
        "registed_at",
    )
    list_display_links = ("username",)
    list_filter = (
        "gender",
        "registed_at",
    )
    search_fields = (
        "username",
        "chat_id",
    )
    readonly_fields = ("registed_at",)
    ordering = ("-registed_at",)
    fieldsets = (
        ("Основная информация", {
            "fields": (
                "username",
                "gender",
                "was_born_at",
            )
        }),
        ("Телега / доп. поля", {
            "fields": (
                "chat_id",
            )
        }),
        ("Системная инфа", {
            "fields": (
                "registed_at",
            )
        }),
    )


class BodyMetricsInline(admin.TabularInline):
    model = BodyMetrics
    extra = 0
    fields = (
        "created_at",
        "weight_kg",
        "body_fat_percent",
        "waist_cm",
        "hips_cm",
        "chest_cm",
        "biceps_cm",
    )
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)


@admin.register(BodyMetrics)
class BodyMetricsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "created_at",
        "weight_kg",
        "body_fat_percent",
        "waist_cm",
        "hips_cm",
    )
    list_display_links = ("id", "user")
    list_filter = ("created_at", "user")
    search_fields = ("user__username", "user__chat_id")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)

    fieldsets = (
        ("Общая информация", {
            "fields": (
                "user",
                "created_at",
                "weight_kg",
                "body_fat_percent",
            )
        }),
        ("Замеры (см)", {
            "fields": (
                "neck_cm",
                "chest_cm",
                "waist_cm",
                "hips_cm",
                "thigh_cm",
                "calf_cm",
                "biceps_cm",
            )
        }),
        ("Дополнительно", {
            "fields": ("note",)
        }),
    )


UserAdmin.inlines = [BodyMetricsInline]
