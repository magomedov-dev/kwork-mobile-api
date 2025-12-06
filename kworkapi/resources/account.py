"""Аккаунт: профиль, баланс, уведомления, настройки.

Имена методов/параметры — заготовки, подтверждаются захватом (Фаза 1).
"""

from __future__ import annotations

from kworkapi.resources.base import Resource


class AccountResource(Resource):
    async def me(self) -> dict:
        """Профиль текущего пользователя."""
        # TODO(capture): подтвердить метод (часто отдаётся вместе с signIn).
        return await self._call("actualAccount")

    async def notifications(self) -> dict:
        """Актуальные уведомления/счётчики."""
        # TODO(capture): подтвердить метод ("actualNotice"?).
        return await self._call("actualNotice")

    async def balance(self) -> dict:
        """Баланс кошелька."""
        # TODO(capture)
        return await self._call("walletInfo")
