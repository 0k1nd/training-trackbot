from apps.core.permissions import IsTelegramBot
from apps.core.throttling import BotRateThrottle
from apps.trainings.api.serializers import FinishWorkoutSerializer, StartWorkoutSerializer
from apps.trainings.models import Exercise, Workout, WorkoutExercise
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

        return Response({"workout_id": workout.id})


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
            return Response({"detail": "no active workout"}, status=404)

        return Response({"id": workout.id})


class AddExerciseToWorkoutView(APIView):
    permission_classes = [IsTelegramBot]

    def post(self, request):
        workout = Workout.objects.get(id=request.data["workout_id"])
        exercise = Exercise.objects.get(id=request.data["exercise_id"])

        last = workout.items.order_by("-order").first()
        next_order = (last.order + 1) if last else 1

        item = WorkoutExercise.objects.create(
            workout=workout,
            exercise=exercise,
            order=next_order,
        )

        return Response({"workout_exercise_id": item.id})


class FinishWorkoutView(APIView):
    permission_classes = [IsTelegramBot]
    throttle_classes = [BotRateThrottle]

    def post(self, request):
        serializer = FinishWorkoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        workout = Workout.objects.get(id=serializer.validated_data["workout_id"])

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
