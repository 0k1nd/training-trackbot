from django.conf import settings
from rest_framework.permissions import BasePermission


class IsTelegramBot(BasePermission):
    def has_permission(self, request, view):
        auth = request.headers.get("Authorization", "")
        prefix = "Bearer"
        if not auth.startswith(prefix):
            return False
        token = auth[len(prefix) :].strip()
        return token == settings.BOT_API_TOKEN
