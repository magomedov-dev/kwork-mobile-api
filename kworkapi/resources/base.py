"""Базовый класс ресурса."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from kworkapi.client import KworkClient


class Resource:
    """Группа методов API. Делегирует низкоуровневые вызовы клиенту."""

    def __init__(self, client: "KworkClient") -> None:
        self._client = client

    async def _call(self, method: str, *, data: dict[str, Any] | None = None, auth: bool = True) -> dict:
        return await self._client.call(method, data=data, auth=auth)
