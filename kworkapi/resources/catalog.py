"""Каталог и поиск: категории, поиск kwork'ов, карточки продавцов.

Имена методов API и параметры — заготовки из prior art, подтверждаются захватом
трафика (Фаза 1). См. research/endpoints.md.
"""

from __future__ import annotations

from kworkapi.resources.base import Resource


class CatalogResource(Resource):
    async def categories(self) -> dict:
        """Дерево категорий каталога."""
        # TODO(capture): подтвердить метод и параметры.
        return await self._call("categories")

    async def search(self, query: str, *, page: int = 1) -> dict:
        """Поиск kwork'ов по строке запроса."""
        # TODO(capture): подтвердить метод ("search"?) и пагинацию.
        return await self._call("search", data={"query": query, "page": page})

    async def kwork(self, kwork_id: int) -> dict:
        """Карточка конкретного kwork по id."""
        # TODO(capture)
        return await self._call("kwork", data={"id": kwork_id})
