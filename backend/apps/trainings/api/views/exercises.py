from collections import defaultdict

from apps.accounts.models import User
from apps.core.permissions import IsTelegramBot
from apps.trainings.models import Exercise
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView


class ExerciseListView(APIView):
    permission_classes = [IsTelegramBot]

    def get(self, request):
        chat_id = request.query_params.get("chat_id")
        user = User.objects.get(chat_id=chat_id)

        exercises = Exercise.objects.filter(Q(author=user) | Q(is_basic=True))

        return Response(
            [
                {
                    "id": e.id,
                    "name": e.name,
                }
                for e in exercises
            ]
        )


class CreateExerciseView(APIView):
    permission_classes = [IsTelegramBot]

    def post(self, request):
        user = User.objects.get(chat_id=request.data["chat_id"])

        exercise = Exercise.objects.create(
            name=request.data["name"],
            primary_muscle=request.data["primary_muscle"],
            author=user,
            is_basic=False,
        )

        return Response({"id": exercise.id})


class ExerciseCatalogView(APIView):
    permission_classes = [IsTelegramBot]

    def get(self, request):
        chat_id = request.query_params.get("chat_id")
        user = User.objects.filter(chat_id=chat_id).first()

        if not user:
            return Response([])

        exercises = Exercise.objects.filter(Q(author=user) | Q(is_basic=True)).order_by(
            "primary_muscle", "name"
        )

        groups = defaultdict(list)

        for exercise in exercises:
            groups[exercise.primary_muscle].append(
                {
                    "id": exercise.id,
                    "name": exercise.name,
                    "primary_muscle": exercise.primary_muscle,
                    "equipment": exercise.equipment,
                    "is_basic": exercise.is_basic,
                }
            )

        return Response(
            [
                {
                    "muscle": muscle,
                    "items": items,
                }
                for muscle, items in groups.items()
            ]
        )


class ExerciseSearchView(APIView):
    permission_classes = [IsTelegramBot]

    def get(self, request):
        chat_id = request.query_params.get("chat_id")
        query = request.query_params.get("q", "").strip()

        user = User.objects.filter(chat_id=chat_id).first()
        if not user:
            return Response([])

        exercises = Exercise.objects.filter(Q(author=user) | Q(is_basic=True))

        if query:
            exercises = exercises.filter(name__icontains=query)

        exercises = exercises.order_by("name")[:20]

        return Response(
            [
                {
                    "id": exercise.id,
                    "name": exercise.name,
                    "primary_muscle": exercise.primary_muscle,
                    "equipment": exercise.equipment,
                    "is_basic": exercise.is_basic,
                }
                for exercise in exercises
            ]
        )
