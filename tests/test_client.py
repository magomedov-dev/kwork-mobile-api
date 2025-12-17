"""Тесты клиента: авторизация, требование токена, восстановление сессии."""

from __future__ import annotations

import httpx
import pytest
import respx

from kworkapi import KworkClient
from kworkapi.auth import Session
from kworkapi.exceptions import KworkAuthError

BASE = "https://api.kwork.ru/"


def _signin_ok(token="TOK", expired=31536000):
    return httpx.Response(
        200,
        json={"success": True, "response": {"token": token, "expired": expired, "need_2fa": False}},
    )


@respx.mock
async def test_login_extracts_token_from_response():
    respx.post(BASE + "signIn").mock(return_value=_signin_ok("TOK"))
    async with KworkClient(base_url=BASE, retry_backoff=0.0) as kw:
        session = await kw.login("user", "pass")
        assert session.token == "TOK"
        assert session.expired == 31536000
        assert session.uad  # сгенерирован
        assert kw.token == "TOK"
        assert kw.is_authenticated


@respx.mock
async def test_login_sends_credentials_and_app_auth():
    route = respx.post(BASE + "signIn").mock(return_value=_signin_ok())
    async with KworkClient(base_url=BASE, retry_backoff=0.0) as kw:
        await kw.login("user@example.com", "secret", recaptcha_pass_token="rt")
        req = route.calls.last.request
        assert req.headers["Authorization"] == "Basic bW9iaWxlX2FwaTpxRnZmUmw3dw=="
        body = req.content
        assert b"login=user%40example.com" in body
        assert b"password=secret" in body
        assert b"recaptcha_pass_token=rt" in body
        assert b"uad=" in body and b"device=" in body
        # без сессии пользовательский токен не подставляется
        assert b"&token=" not in body and not body.startswith(b"token=")


@respx.mock
async def test_login_without_token_raises():
    respx.post(BASE + "signIn").mock(return_value=httpx.Response(200, json={"success": True}))
    async with KworkClient(base_url=BASE, retry_backoff=0.0) as kw:
        with pytest.raises(KworkAuthError):
            await kw.login("user", "pass")


async def test_authorized_call_without_session_raises():
    async with KworkClient(base_url=BASE, retry_backoff=0.0) as kw:
        with pytest.raises(KworkAuthError):
            await kw.account.me()


@respx.mock
async def test_resource_call_sends_token_and_common_fields():
    route = respx.post(BASE + "actor").mock(
        return_value=httpx.Response(200, json={"success": True, "response": {"id": 1}})
    )
    sess = Session(token="ABC", uad="DEADBEEF")
    async with KworkClient.from_session(sess, base_url=BASE, retry_backoff=0.0) as kw:
        await kw.account.me()
        body = route.calls.last.request.content
        assert b"token=ABC" in body
        assert b"uad=DEADBEEF" in body
        assert b"device=" in body


@respx.mock
async def test_session_uad_propagated_to_transport():
    sess = Session(token="T", uad="MYUAD123")
    async with KworkClient.from_session(sess, base_url=BASE) as kw:
        assert kw._transport.uad == "MYUAD123"


def test_session_roundtrip():
    sess = Session(token="t", uad="u", slrememberme="s", expired=10, need_2fa=False)
    assert Session.from_dict(sess.to_dict()) == sess
