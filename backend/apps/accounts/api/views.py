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
        return BodyMetrics.objects.filter(user=user).order_by("-created_at", "-id")

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        try:
            limit = int(request.query_params.get("limit", 5))
        except (TypeError, ValueError):
            limit = 5

        try:
            offset = int(request.query_params.get("offset", 0))
        except (TypeError, ValueError):
            offset = 0

        if limit < 1:
            limit = 5
        if limit > 20:
            limit = 20
        if offset < 0:
            offset = 0

        total = queryset.count()
        items = queryset[offset : offset + limit]

        serializer = self.get_serializer(items, many=True)

        next_offset = offset + limit if offset + limit < total else None
        prev_offset = offset - limit if offset - limit >= 0 else None

        return Response(
            {
                "count": total,
                "limit": limit,
                "offset": offset,
                "next_offset": next_offset,
                "prev_offset": prev_offset,
                "results": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def get_object(self):
        queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.kwargs["pk"])

    def perform_create(self, serializer):
        user = self.get_user()
        serializer.save(user=user)
