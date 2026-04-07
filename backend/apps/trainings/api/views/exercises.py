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
