"""Сообщения и чаты: список диалогов, история переписки, отправка сообщений.

Имена методов/параметры — заготовки из prior art (getDialogs/inboxes/dialog),
подтверждаются захватом (Фаза 1).
"""

from __future__ import annotations

from kworkapi.resources.base import Resource


class MessagesResource(Resource):
    async def dialogs(self, *, page: int = 1) -> dict:
        """Список диалогов (чатов)."""
        # TODO(capture): подтвердить метод ("getDialogs"?).
        return await self._call("getDialogs", data={"page": page})

    async def history(self, username: str, *, page: int = 1) -> dict:
        """История переписки с конкретным пользователем."""
        # TODO(capture): подтвердить метод ("dialog"?) и идентификатор собеседника
        # (username или user_id).
        return await self._call("dialog", data={"username": username, "page": page})

    async def send(self, username: str, text: str) -> dict:
        """Отправить сообщение пользователю."""
        # TODO(capture): подтвердить метод ("inboxCreate"?) и поля.
        return await self._call("inboxCreate", data={"username": username, "text": text})
