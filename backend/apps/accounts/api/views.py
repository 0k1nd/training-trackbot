from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.accounts.api.serializers import RegistrationSerializer
from apps.core.permissions import IsTelegramBot

import logging


logger = logging.getLogger(__name__)

class RegistrationView(APIView):
    permission_classes = [IsTelegramBot]

    def get(self, request, *args, **kwargs):
        logger.info("Registration GET data: %s", request.data)
        return Response({"detail": "OK"}, status=200)

    def post(self, request, *args, **kwargs):
        logger.info("Registration POST data: %s", request.data)
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            {
                "id": user.id,
                "chat_id": user.chat_id,
                "username": user.username,
            },
            status=status.HTTP_200_OK,
        )
