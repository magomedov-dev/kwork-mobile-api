"""Заказы: активные/завершённые заказы пользователя, их статусы.

Имена методов/параметры — заготовки, подтверждаются захватом (Фаза 1).
"""

from __future__ import annotations

from kworkapi.resources.base import Resource


class OrdersResource(Resource):
    async def list(self, *, page: int = 1) -> dict:
        """Список заказов пользователя."""
        # TODO(capture): подтвердить метод ("orders"?) и фильтр по статусу.
        return await self._call("orders", data={"page": page})

    async def get(self, order_id: int) -> dict:
        """Детали заказа."""
        # TODO(capture)
        return await self._call("order", data={"id": order_id})
