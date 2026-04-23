from apps.trainings.api.views import (
    AddExerciseToWorkoutView,
    AddSetView,
    CreateExerciseView,
    CurrentWorkoutView,
    ExerciseListView,
    FinishWorkoutExerciseView,
    FinishWorkoutView,
    StartWorkoutView,
    WorkoutExerciseSetsView,
)
from django.urls import path

urlpatterns = [
    path("workouts/start/", StartWorkoutView.as_view(), name="bot-workout-start"),
    path("workouts/current/", CurrentWorkoutView.as_view(), name="bot-workout-current"),
    path(
        "workouts/add-exercise/",
        AddExerciseToWorkoutView.as_view(),
        name="bot-workout-add-exercise",
    ),
    path("workouts/finish/", FinishWorkoutView.as_view(), name="bot-workout-finish"),
    path("exercises/", ExerciseListView.as_view(), name="bot-exercise-list"),
    path("exercises/create/", CreateExerciseView.as_view(), name="bot-exercise-create"),
    path("sets/add/", AddSetView.as_view(), name="bot-set-add"),
    path(
        "workout-exercises/<int:pk>/sets/",
        WorkoutExerciseSetsView.as_view(),
        name="bot-workout-exercise-sets",
    ),
    path(
        "workout-exercises/finish/",
        FinishWorkoutExerciseView.as_view(),
        name="bot-workout-exercise-finish",
    ),
]
