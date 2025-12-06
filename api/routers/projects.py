"""REST: биржа проектов."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from api.deps import get_client
from kworkapi import KworkClient

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("")
async def feed(
    client: Annotated[KworkClient, Depends(get_client)],
    page: int = 1,
    category: int | None = None,
) -> dict:
    """Лента проектов на бирже."""
    return await client.projects.feed(page=page, category=category)


@router.get("/{project_id}")
async def get_project(
    project_id: int,
    client: Annotated[KworkClient, Depends(get_client)],
) -> dict:
    """Детали проекта."""
    return await client.projects.get(project_id)
