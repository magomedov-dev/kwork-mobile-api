"""Аккаунт: профиль, баланс, уведомления, настройки.

Имена методов/параметры — заготовки, подтверждаются захватом (Фаза 1).
"""

from __future__ import annotations

from kworkapi.resources.base import Resource


class AccountResource(Resource):
    async def me(self) -> dict:
        """Профиль и состояние текущего пользователя (баланс, счётчики и т.д.).

        Эндпоинт `/actor` — подтверждён живым трафиком (см. docs/06).
        """
        return await self._call("actor")

    async def notifications(self, *, page: int = 1) -> dict:
        """Лента уведомлений пользователя (`/notificationsFetch`)."""
        return await self._call("notificationsFetch", data={"page": page})
