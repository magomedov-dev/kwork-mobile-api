"""HTTP-транспорт: единая точка общения с api.kwork.ru.

Все детали, которые нужно подтвердить захватом трафика (Фаза 1), вынесены в
константы/параметры с пометкой TODO(capture). После реверса APK сюда подставляются
реальные значения: base_url, статичный Authorization-токен приложения, User-Agent,
схема подписи (если есть).
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any

import httpx

from kworkapi.exceptions import (
    KworkAPIError,
    KworkAuthError,
    KworkError,
    KworkRateLimitError,
)

logger = logging.getLogger("kworkapi.transport")

# TODO(capture): подтвердить базовый URL мобильного API при захвате трафика.
DEFAULT_BASE_URL = "https://api.kwork.ru/"

# TODO(capture): извлечь из APK (jadx) статичный заголовок Authorization: Basic <...>,
# которым приложение подписывает ВСЕ запросы (это не пользовательский токен, а
# идентификатор клиента-приложения). Оставлен пустым намеренно — заполняется из
# research/endpoints.md после Фазы 1.
DEFAULT_APP_AUTHORIZATION = ""

# TODO(capture): подтвердить User-Agent приложения (виден в перехвате).
DEFAULT_USER_AGENT = "kwork-android"


class Transport:
    """Тонкая обёртка над httpx.AsyncClient под специфику мобильного API kwork.

    Особенности приватного API (по prior art, требует подтверждения захватом):
      * методы вызываются как POST на ``{base_url}{method}``;
      * статичный заголовок ``Authorization: Basic <app token>`` на каждый запрос;
      * пользовательский ``token`` передаётся в теле формы (data), а не в заголовке;
      * успех/ошибка определяется полем ``success`` в JSON-ответе.
    """

    def __init__(
        self,
        *,
        base_url: str = DEFAULT_BASE_URL,
        app_authorization: str = DEFAULT_APP_AUTHORIZATION,
        user_agent: str = DEFAULT_USER_AGENT,
        timeout: float = 20.0,
        max_retries: int = 3,
        retry_backoff: float = 0.5,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        self.base_url = base_url
        self.app_authorization = app_authorization
        self.max_retries = max_retries
        self.retry_backoff = retry_backoff

        headers = {"User-Agent": user_agent}
        if app_authorization:
            headers["Authorization"] = app_authorization

        self._owns_client = client is None
        self._client = client or httpx.AsyncClient(
            base_url=base_url,
            headers=headers,
            timeout=timeout,
        )

    async def call(
        self,
        method: str,
        *,
        data: dict[str, Any] | None = None,
        token: str | None = None,
    ) -> dict[str, Any]:
        """Вызвать метод API и вернуть полезную нагрузку (распарсенный JSON).

        :param method: имя метода API, например ``"signIn"`` или ``"projects"``.
        :param data: поля формы запроса.
        :param token: пользовательский токен сессии (подставляется в data).
        """
        payload: dict[str, Any] = dict(data or {})
        if token is not None:
            payload.setdefault("token", token)

        last_exc: Exception | None = None
        for attempt in range(1, self.max_retries + 1):
            try:
                response = await self._client.post(method, data=payload)
            except httpx.TransportError as exc:  # сетевые сбои — повторяем
                last_exc = exc
                logger.warning("Сетевая ошибка (%s/%s) на %s: %s", attempt, self.max_retries, method, exc)
                await asyncio.sleep(self.retry_backoff * attempt)
                continue

            if response.status_code == 429:
                # Бэкофф и повтор на rate-limit.
                if attempt < self.max_retries:
                    await asyncio.sleep(self.retry_backoff * attempt * 2)
                    continue
                raise KworkRateLimitError("Rate limit (HTTP 429)", code=429)

            return self._parse(method, response)

        raise KworkError(f"Не удалось выполнить запрос {method}: {last_exc}")

    def _parse(self, method: str, response: httpx.Response) -> dict[str, Any]:
        try:
            body = response.json()
        except ValueError as exc:
            raise KworkAPIError(
                f"Не-JSON ответ от {method} (HTTP {response.status_code})",
                code=response.status_code,
                payload=response.text[:500],
            ) from exc

        # TODO(capture): уточнить реальную форму ответа об ошибке (поля success/
        # error/error_code/message) по захвату — ниже наиболее вероятная схема.
        if isinstance(body, dict) and body.get("success") is False:
            message = str(body.get("error") or body.get("message") or "Ошибка API")
            code = body.get("error_code") or body.get("code")
            low = message.lower()
            if "token" in low or "auth" in low or "авториз" in low:
                raise KworkAuthError(message, code=code, payload=body)
            raise KworkAPIError(message, code=code, payload=body)

        if response.status_code >= 400:
            raise KworkAPIError(
                f"HTTP {response.status_code} от {method}",
                code=response.status_code,
                payload=body,
            )

        return body

    async def aclose(self) -> None:
        if self._owns_client:
            await self._client.aclose()
