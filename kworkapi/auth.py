"""Авторизация и управление токеном сессии.

Схема (по prior art, подтвердить захватом в Фазе 1): POST на метод ``signIn`` с
полями login/password (+ возможно phone), в ответе — пользовательский ``token``,
который дальше передаётся в теле каждого запроса.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from kworkapi.exceptions import KworkAuthError

if TYPE_CHECKING:
    from kworkapi.transport import Transport


@dataclass
class Session:
    """Состояние авторизованной сессии."""

    token: str
    user_id: int | None = None
    raw: dict | None = None

    @property
    def is_authenticated(self) -> bool:
        return bool(self.token)


class Auth:
    """Логика входа. Хранение токена снаружи — забота вызывающего кода/клиента."""

    def __init__(self, transport: "Transport") -> None:
        self._transport = transport

    async def sign_in(self, login: str, password: str, *, phone: str = "") -> Session:
        """Войти по логину и паролю, вернуть Session с токеном.

        TODO(capture): подтвердить имя метода ("signIn") и набор полей формы, а также
        путь к токену в ответе. Ниже — наиболее вероятная схема из prior art.
        """
        body = await self._transport.call(
            "signIn",
            data={"login": login, "password": password, "phone": phone},
        )

        token = self._extract_token(body)
        if not token:
            raise KworkAuthError("В ответе signIn не найден token", payload=body)

        user_id = None
        if isinstance(body, dict):
            data = body.get("response") or body.get("data") or body
            if isinstance(data, dict):
                user_id = data.get("id") or data.get("user_id")

        return Session(token=token, user_id=user_id, raw=body)

    @staticmethod
    def _extract_token(body: dict) -> str | None:
        # TODO(capture): уточнить точный путь к токену по реальному ответу.
        if not isinstance(body, dict):
            return None
        if "token" in body:
            return body["token"]
        for key in ("response", "data", "result"):
            section = body.get(key)
            if isinstance(section, dict) and section.get("token"):
                return section["token"]
        return None
