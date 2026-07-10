"""Tests for the LittleSis API client. httpx.AsyncClient is mocked — no network."""
from __future__ import annotations

import asyncio

import httpx
import pytest

from ratchet_mcp import littlesis


class _Resp:
    def __init__(self, payload, boom=None):
        self._payload, self._boom = payload, boom

    def raise_for_status(self):
        if self._boom:
            raise self._boom

    def json(self):
        return self._payload


class _Client:
    """Fake AsyncClient context manager whose .get returns a queued response (or raises)."""
    def __init__(self, resp):
        self._resp = resp

    async def __aenter__(self):
        return self

    async def __aexit__(self, *a):
        return False

    async def get(self, url, params=None):
        if isinstance(self._resp, Exception):
            raise self._resp
        return self._resp


def _patch(monkeypatch, resp):
    monkeypatch.setattr(littlesis.httpx, "AsyncClient", lambda *a, **k: _Client(resp))


def test_search_entity_ok(monkeypatch):
    _patch(monkeypatch, _Resp({"data": [{"id": 1}, {"id": 2}, {"id": 3}]}))
    out = asyncio.run(littlesis.search_entity("rubin", limit=2))
    assert [r["id"] for r in out] == [1, 2]


def test_search_entity_http_error_returns_empty(monkeypatch):
    _patch(monkeypatch, _Resp({}, boom=httpx.HTTPError("boom")))
    assert asyncio.run(littlesis.search_entity("x")) == []


def test_search_entity_no_data_key(monkeypatch):
    _patch(monkeypatch, _Resp({}))
    assert asyncio.run(littlesis.search_entity("x")) == []


def test_get_relationships_ok(monkeypatch):
    _patch(monkeypatch, _Resp({"data": [{"id": 9}]}))
    out = asyncio.run(littlesis.get_relationships(123, limit=20))
    assert out == [{"id": 9}]


def test_get_relationships_error_returns_empty(monkeypatch):
    _patch(monkeypatch, _Resp({}, boom=httpx.TimeoutException("slow")))
    assert asyncio.run(littlesis.get_relationships(123)) == []


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
