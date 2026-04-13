import hashlib
import hmac
import json
import time

import aiohttp

from app.api.exceptions import (
    BackendApiError,
    BackendUnauthorizedError,
    BackendValidationError,
)


class BackendApiClient:
    def __init__(self, base_url: str, bot_api_token: str):
        self.base_url = base_url.rstrip("/")
        self.bot_api_token = bot_api_token

    def _build_signature(self, timestamp: str, body: bytes) -> str:
        return hmac.new(
            self.bot_api_token.encode(),
            timestamp.encode() + body,
            hashlib.sha256,
        ).hexdigest()

    async def _request(
        self,
        method: str,
        path: str,
        payload: dict | None = None,
        params: dict | None = None,
    ):
        url = f"{self.base_url}{path}"
        body = b""
        headers = {}

        if payload is not None:
            body = json.dumps(payload, separators=(",", ":")).encode()
            headers["Content-Type"] = "application/json"

        timestamp = str(int(time.time()))
        headers["X-Timestamp"] = timestamp
        headers["X-Signature"] = self._build_signature(timestamp, body)

        timeout = aiohttp.ClientTimeout(total=15)

        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.request(
                method=method,
                url=url,
                params=params,
                data=body if payload is not None else None,
                headers=headers,
            ) as response:
                content_type = response.headers.get("Content-Type", "")
                is_json = "application/json" in content_type

                if is_json:
                    data = await response.json()
                else:
                    data = await response.text()

                if response.status in (401, 403):
                    raise BackendUnauthorizedError(data)

                if response.status == 400:
                    raise BackendValidationError(data)

                if response.status >= 400:
                    raise BackendApiError(data)

                return data

    async def register_user(
        self,
        chat_id: int,
        username: str | None,
        first_name: str | None,
        last_name: str | None,
    ):
        return await self._request(
            method="POST",
            path="/api/users/register/",
            payload={
                "chat_id": chat_id,
                "username": username,
                "first_name": first_name,
                "last_name": last_name,
            },
        )

    async def list_body_metrics(self, chat_id: int, limit: int = 5, offset: int = 0):
        return await self._request(
            method="GET",
            path="/api/users/body-metrics/",
            params={
                "chat_id": chat_id,
                "limit": limit,
                "offset": offset,
            },
        )

    async def create_body_metric(self, chat_id: int, payload: dict):
        body = {"chat_id": chat_id, **payload}
        return await self._request(
            method="POST",
            path="/api/users/body-metrics/",
            payload=body,
        )

    async def delete_body_metric(self, chat_id: int, metric_id: int):
        return await self._request(
            method="DELETE",
            path=f"/api/users/body-metrics/{metric_id}/",
            payload={"chat_id": chat_id},
        )
