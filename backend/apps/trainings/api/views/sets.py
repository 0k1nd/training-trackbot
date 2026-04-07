from apps.core.permissions import IsTelegramBot
from apps.core.throttling import BotRateThrottle
from apps.trainings.api.serializers import AddSetSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class AddSetView(APIView):
    permission_classes = [IsTelegramBot]
    throttle_classes = [BotRateThrottle]

    def post(self, request):
        serializer = AddSetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        obj = serializer.save()

        return Response(
            {
                "id": obj.id,
                "set_number": obj.set_number,
                "weight": obj.weight,
                "reps": obj.reps,
                "difficulty": obj.difficulty,
            },
            status=status.HTTP_201_CREATED,
        )
