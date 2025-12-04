"""Тесты клиента: авторизация, требование токена, проброс в ресурсы."""

from __future__ import annotations

import httpx
import pytest
import respx

from kworkapi import KworkClient
from kworkapi.exceptions import KworkAuthError

BASE = "https://api.kwork.ru/"


@respx.mock
async def test_login_extracts_token_and_sets_session():
    respx.post(BASE + "signIn").mock(
        return_value=httpx.Response(200, json={"success": True, "token": "TOK", "id": 42})
    )
    async with KworkClient(base_url=BASE, retry_backoff=0.0) as kw:
        session = await kw.login("user", "pass")
        assert session.token == "TOK"
        assert session.user_id == 42
        assert kw.token == "TOK"


@respx.mock
async def test_login_token_nested_in_response():
    respx.post(BASE + "signIn").mock(
        return_value=httpx.Response(200, json={"success": True, "response": {"token": "NESTED"}})
    )
    async with KworkClient(base_url=BASE, retry_backoff=0.0) as kw:
        session = await kw.login("user", "pass")
        assert session.token == "NESTED"


@respx.mock
async def test_login_without_token_raises():
    respx.post(BASE + "signIn").mock(return_value=httpx.Response(200, json={"success": True}))
    async with KworkClient(base_url=BASE, retry_backoff=0.0) as kw:
        with pytest.raises(KworkAuthError):
            await kw.login("user", "pass")


async def test_authorized_call_without_session_raises():
    async with KworkClient(base_url=BASE, retry_backoff=0.0) as kw:
        with pytest.raises(KworkAuthError):
            await kw.projects.feed()


@respx.mock
async def test_resource_call_sends_token():
    route = respx.post(BASE + "projects").mock(
        return_value=httpx.Response(200, json={"success": True, "projects": []})
    )
    async with KworkClient(base_url=BASE, token="ABC", retry_backoff=0.0) as kw:
        await kw.projects.feed(page=2)
        content = route.calls.last.request.content
        assert b"token=ABC" in content
        assert b"page=2" in content
