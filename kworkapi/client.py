"""KworkClient — главная точка входа в библиотеку."""

from __future__ import annotations

from types import TracebackType

from kworkapi.auth import Auth, Session
from kworkapi.exceptions import KworkAuthError
from kworkapi.resources.account import AccountResource
from kworkapi.resources.catalog import CatalogResource
from kworkapi.resources.messages import MessagesResource
from kworkapi.resources.orders import OrdersResource
from kworkapi.resources.projects import ProjectsResource
from kworkapi.transport import Transport


class KworkClient:
    """Асинхронный клиент приватного API kwork.ru.

    Пример::

        async with KworkClient() as kw:
            await kw.login("user@example.com", "secret")
            projects = await kw.projects.feed()
    """

    def __init__(
        self,
        *,
        token: str | None = None,
        transport: Transport | None = None,
        **transport_kwargs,
    ) -> None:
        self._transport = transport or Transport(**transport_kwargs)
        self._auth = Auth(self._transport)
        self.session: Session | None = Session(token=token) if token else None

        # Группы методов (ресурсы).
        self.catalog = CatalogResource(self)
        self.projects = ProjectsResource(self)
        self.orders = OrdersResource(self)
        self.messages = MessagesResource(self)
        self.account = AccountResource(self)

    # --- авторизация -----------------------------------------------------

    async def login(self, login: str, password: str, *, phone: str = "") -> Session:
        """Войти по логину/паролю и сохранить сессию в клиенте."""
        self.session = await self._auth.sign_in(login, password, phone=phone)
        return self.session

    @property
    def token(self) -> str | None:
        return self.session.token if self.session else None

    # --- низкоуровневый вызов (используется ресурсами) -------------------

    async def call(self, method: str, *, data: dict | None = None, auth: bool = True) -> dict:
        """Вызвать метод API. При ``auth=True`` требуется активная сессия."""
        token = None
        if auth:
            if not self.session or not self.session.is_authenticated:
                raise KworkAuthError(f"Метод {method} требует авторизации — сначала login()")
            token = self.session.token
        return await self._transport.call(method, data=data, token=token)

    # --- управление жизненным циклом ------------------------------------

    async def aclose(self) -> None:
        await self._transport.aclose()

    async def __aenter__(self) -> "KworkClient":
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        await self.aclose()
