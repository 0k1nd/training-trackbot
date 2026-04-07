import hashlib
import hmac
import time

from django.conf import settings
from rest_framework.permissions import BasePermission


class IsTelegramBot(BasePermission):
    MAX_DRIFT_SECONDS = 60

    def has_permission(self, request, view):
        signature = request.headers.get("X-Signature")
        timestamp = request.headers.get("X-Timestamp")

        if not signature or not timestamp:
            return False

        try:
            timestamp = int(timestamp)
        except ValueError:
            return False

        if abs(time.time() - timestamp) > self.MAX_DRIFT_SECONDS:
            return False

        expected = self._build_signature(timestamp, request.body)

        return hmac.compare_digest(signature, expected)

    def _build_signature(self, timestamp: int, body: bytes) -> str:
        return hmac.new(
            settings.BOT_API_TOKEN.encode(),
            str(timestamp).encode() + body,
            hashlib.sha256,
        ).hexdigest()
