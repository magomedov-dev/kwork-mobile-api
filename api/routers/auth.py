"""REST: авторизация."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from api.deps import get_anon_client
from kworkapi import KworkClient

router = APIRouter(prefix="/auth", tags=["auth"])


class LoginRequest(BaseModel):
    login: str
    password: str
    phone: str = ""


class LoginResponse(BaseModel):
    token: str
    user_id: int | None = None


@router.post("/login", response_model=LoginResponse)
async def login(
    body: LoginRequest,
    client: Annotated[KworkClient, Depends(get_anon_client)],
) -> LoginResponse:
    """Войти по логину/паролю и получить токен сессии kwork."""
    session = await client.login(body.login, body.password, phone=body.phone)
    return LoginResponse(token=session.token, user_id=session.user_id)
