import logging

from apps.accounts.api.serializers import BodyMetricsSerializer, RegistrationSerializer
from apps.accounts.models import BodyMetrics, User
from apps.core.permissions import IsTelegramBot
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

logger = logging.getLogger(__name__)


class RegistrationView(APIView):
    permission_classes = [IsTelegramBot]

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


class BodyMetricsViewSet(viewsets.ModelViewSet):
    serializer_class = BodyMetricsSerializer
    permission_classes = [IsTelegramBot]

    def get_user(self):
        chat_id = self.request.query_params.get("chat_id") or self.request.data.get("chat_id")
        if not chat_id:
            return None
        return get_object_or_404(User, chat_id=chat_id)

    def get_queryset(self):
        user = self.get_user()
        if user is None:
            return BodyMetrics.objects.none()
        return BodyMetrics.objects.filter(user=user).order_by("-date", "-id")

    def perform_create(self, serializer):
        user = self.get_user()
        serializer.save(user=user)
