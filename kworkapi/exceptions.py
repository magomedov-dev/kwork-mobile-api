"""Иерархия исключений библиотеки."""

from __future__ import annotations


class KworkError(Exception):
    """Базовое исключение всех ошибок KworkAPI."""


class KworkAPIError(KworkError):
    """API вернул ответ с признаком ошибки (success=false) или неожиданный код."""

    def __init__(self, message: str, *, code: int | None = None, payload: object | None = None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.payload = payload


class KworkAuthError(KworkAPIError):
    """Ошибка авторизации: неверные данные, протухший/отсутствующий токен."""


class KworkRateLimitError(KworkAPIError):
    """Слишком много запросов — сработал rate-limit или анти-бот."""
