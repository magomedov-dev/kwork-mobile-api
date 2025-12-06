"""Точка входа FastAPI-сервиса.

Запуск:  uvicorn api.main:app --reload
Доки:    http://127.0.0.1:8000/docs
"""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.deps import close_clients
from api.routers import auth, catalog, projects


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await close_clients()


app = FastAPI(
    title="KworkAPI",
    description="Неофициальный REST поверх приватного API kwork.ru.",
    version="0.0.1",
    lifespan=lifespan,
)

app.include_router(auth.router)
app.include_router(catalog.router)
app.include_router(projects.router)


@app.get("/health", tags=["service"])
async def health() -> dict:
    return {"status": "ok"}
