"""Биржа проектов: лента заказов от покупателей и отклики исполнителя.

Имена методов/параметры — заготовки, подтверждаются захватом (Фаза 1).
"""

from __future__ import annotations

from kworkapi.resources.base import Resource


class ProjectsResource(Resource):
    async def feed(self, *, page: int = 1, category: int | None = None) -> dict:
        """Лента проектов (заказов покупателей) на бирже."""
        # TODO(capture): подтвердить метод ("projects"?) и фильтры.
        data: dict = {"page": page}
        if category is not None:
            data["category"] = category
        return await self._call("projects", data=data)

    async def get(self, project_id: int) -> dict:
        """Детали проекта."""
        # TODO(capture)
        return await self._call("project", data={"id": project_id})

    async def offer(self, project_id: int, message: str, *, price: int | None = None) -> dict:
        """Откликнуться на проект."""
        # TODO(capture): подтвердить метод отклика и поля (цена/срок).
        data: dict = {"project_id": project_id, "message": message}
        if price is not None:
            data["price"] = price
        return await self._call("offer", data=data)
