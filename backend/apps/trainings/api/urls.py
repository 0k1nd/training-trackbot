from apps.trainings.api.views import (
    AddExerciseToWorkoutView,
    AddSetView,
    CreateExerciseView,
    CurrentWorkoutView,
    ExerciseListView,
    FinishWorkoutView,
    StartWorkoutView,
)
from django.urls import path

urlpatterns = [
    path("workouts/start/", StartWorkoutView.as_view()),
    path("workouts/current/", CurrentWorkoutView.as_view()),
    path("workouts/add-exercise/", AddExerciseToWorkoutView.as_view()),
    path("workouts/finish/", FinishWorkoutView.as_view()),
    path("exercises/", ExerciseListView.as_view()),
    path("exercises/create/", CreateExerciseView.as_view()),
    path("sets/add/", AddSetView.as_view()),
]
