from django.contrib import admin

from apps.trainings.models import Workout, WorkoutExercise, Set, Exercise


class WorkoutExerciseInline(admin.TabularInline):
    model = WorkoutExercise
    extra = 0


class SetInline(admin.TabularInline):
    model = Set
    extra = 0


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ("name", "primary_muscle", "secondary_muscle", "equipment", "is_basic", "author")
    list_filter = ("primary_muscle", "equipment", "is_basic")
    search_fields = ("name", "description")
    autocomplete_fields = ("author",)

    def save_model(self, request, obj, form, change):
        if not change or obj.author_id is None:
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "workout_type", "created_at")
    list_filter = ("workout_type", "created_at")
    search_fields = ("user__username", "user__telegram_id")
    inlines = [WorkoutExerciseInline]


@admin.register(WorkoutExercise)
class WorkoutExerciseAdmin(admin.ModelAdmin):
    list_display = ("id", "workout", "exercise", "order")
    list_filter = ("exercise", "workout__workout_type")
    search_fields = ("workout__user__username", "exercise__name")


@admin.register(Set)
class SetAdmin(admin.ModelAdmin):
    list_display = ("id", "workout_exercise", "set_number", "weight", "reps", "difficulty", "created_at")
    list_filter = ("difficulty", "workout_exercise__exercise")
    search_fields = ("workout_exercise__workout__user__username",)