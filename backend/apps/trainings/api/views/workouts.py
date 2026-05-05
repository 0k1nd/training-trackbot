from apps.accounts.models import User
from apps.core.permissions import IsTelegramBot
from apps.core.throttling import BotRateThrottle
from apps.trainings.api.serializers import FinishWorkoutSerializer, StartWorkoutSerializer
from apps.trainings.models import Exercise, Workout, WorkoutExercise
from django.db.models import Q
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class StartWorkoutView(APIView):
    permission_classes = [IsTelegramBot]
    throttle_classes = [BotRateThrottle]

    def post(self, request):
        serializer = StartWorkoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        workout = serializer.save()

        return Response({"workout_id": workout.id}, status=status.HTTP_201_CREATED)


class CurrentWorkoutView(APIView):
    permission_classes = [IsTelegramBot]

    def get(self, request):
        chat_id = request.query_params.get("chat_id")

        workout = (
            Workout.objects.filter(user__chat_id=chat_id, finished_at__isnull=True)
            .order_by("-created_at")
            .first()
        )

        if not workout:
            return Response({"detail": "no active workout"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"id": workout.id})


class AddExerciseToWorkoutView(APIView):
    permission_classes = [IsTelegramBot]

    def post(self, request):
        chat_id = request.data["chat_id"]
        workout_id = request.data["workout_id"]
        exercise_id = request.data["exercise_id"]

        workout = Workout.objects.filter(
            id=workout_id,
            user__chat_id=chat_id,
            finished_at__isnull=True,
        ).first()
        if not workout:
            return Response(
                {"detail": "active workout not found"}, status=status.HTTP_404_NOT_FOUND
            )

        user = User.objects.get(chat_id=chat_id)

        exercise = Exercise.objects.filter(
            Q(id=exercise_id),
            Q(author=user) | Q(is_basic=True),
        ).first()

        if not exercise:
            return Response({"detail": "exercise not found"}, status=status.HTTP_404_NOT_FOUND)

        last = workout.items.order_by("-order").first()
        next_order = last.order + 1 if last else 1

        item = WorkoutExercise.objects.create(
            workout=workout,
            exercise=exercise,
            order=next_order,
        )

        return Response(
            {
                "workout_exercise_id": item.id,
                "exercise_id": exercise.id,
                "exercise_name": exercise.name,
                "order": item.order,
            },
            status=status.HTTP_201_CREATED,
        )


class WorkoutExerciseSetsView(APIView):
    permission_classes = [IsTelegramBot]

    def get(self, request, pk: int):
        chat_id = request.query_params.get("chat_id")

        workout_exercise = (
            WorkoutExercise.objects.filter(
                id=pk,
                workout__user__chat_id=chat_id,
            )
            .select_related("exercise")
            .prefetch_related("sets")
            .first()
        )

        if not workout_exercise:
            return Response(
                {"detail": "workout exercise not found"}, status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            {
                "id": workout_exercise.id,
                "exercise": {
                    "id": workout_exercise.exercise.id,
                    "name": workout_exercise.exercise.name,
                },
                "sets": [
                    {
                        "id": s.id,
                        "set_number": s.set_number,
                        "weight": s.weight,
                        "reps": s.reps,
                        "difficulty": s.difficulty,
                    }
                    for s in workout_exercise.sets.all().order_by("set_number")
                ],
            }
        )


class FinishWorkoutExerciseView(APIView):
    permission_classes = [IsTelegramBot]

    def post(self, request):
        chat_id = request.data.get("chat_id")
        workout_exercise_id = request.data.get("workout_exercise_id")

        workout_exercise = WorkoutExercise.objects.filter(
            id=workout_exercise_id,
            workout__user__chat_id=chat_id,
            workout__finished_at__isnull=True,
            finished_at__isnull=True,
        ).first()

        if not workout_exercise:
            return Response(
                {"detail": "workout exercise not found"}, status=status.HTTP_404_NOT_FOUND
            )

        workout_exercise.finished_at = timezone.now()
        workout_exercise.save(update_fields=["finished_at"])

        return Response(
            {
                "id": workout_exercise.id,
                "status": "finished",
                "finished_at": workout_exercise.finished_at,
            },
            status=status.HTTP_200_OK,
        )


class FinishWorkoutView(APIView):
    permission_classes = [IsTelegramBot]
    throttle_classes = [BotRateThrottle]

    def post(self, request):
        serializer = FinishWorkoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        workout = serializer.validated_data["workout"]

        if workout.finished_at is not None:
            return Response(
                {"detail": "workout already finished"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        workout.finished_at = timezone.now()
        workout.save(update_fields=["finished_at"])

        return Response(
            {
                "id": workout.id,
                "finished_at": workout.finished_at,
                "status": "finished",
            },
            status=status.HTTP_200_OK,
        )


class WorkoutListView(APIView):
    permission_classes = [IsTelegramBot]

    def get(self, request):
        chat_id = request.query_params.get("chat_id")

        workouts = (
            Workout.objects.filter(user__chat_id=chat_id)
            .prefetch_related("items__exercise", "items__sets")
            .order_by("-created_at")[:20]
        )

        return Response(
            [
                {
                    "id": workout.id,
                    "workout_type": workout.workout_type,
                    "created_at": workout.created_at,
                    "finished_at": workout.finished_at,
                    "exercises_count": workout.items.count(),
                    "sets_count": sum(item.sets.count() for item in workout.items.all()),
                }
                for workout in workouts
            ]
        )
