"""Зависимости FastAPI: построение клиента kworkapi из токена запроса."""

from __future__ import annotations

from typing import Annotated

from fastapi import Header, HTTPException

from kworkapi import KworkClient
from kworkapi.transport import Transport

# Один общий транспорт (httpx-пул) на сервис; токен пользователя передаётся per-request.
_transport = Transport()


def get_client(
    x_kwork_token: Annotated[str | None, Header(alias="X-Kwork-Token")] = None,
) -> KworkClient:
    """Клиент для авторизованных эндпоинтов: токен берётся из заголовка X-Kwork-Token."""
    if not x_kwork_token:
        raise HTTPException(status_code=401, detail="Нужен заголовок X-Kwork-Token")
    return KworkClient(token=x_kwork_token, transport=_transport)


def get_anon_client() -> KworkClient:
    """Клиент без токена — для логина."""
    return KworkClient(transport=_transport)


async def close_clients() -> None:
    await _transport.aclose()
