"""Базовая pydantic-модель для ответов kwork."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class KworkModel(BaseModel):
    """База для всех моделей.

    ``extra="allow"`` — сохраняем неизвестные поля, пока схема API не зафиксирована
    захватом (Фаза 1). ``populate_by_name`` — допускаем заполнение и по alias, и по имени.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)
