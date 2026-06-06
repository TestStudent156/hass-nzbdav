"""Async client for the NZBDav SABnzbd-compatible API."""
from __future__ import annotations

import asyncio
from typing import Any

import aiohttp
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession


class NzbDavError(Exception):
    """Base error."""


class CannotConnect(NzbDavError):
    """Cannot reach the server."""


class InvalidAuth(NzbDavError):
    """API key rejected."""


class NzbDavClient:
    """Talks to the nzbdav SABnzbd-compatible API."""

    def __init__(
        self,
        hass: HomeAssistant,
        host: str,
        port: int,
        ssl: bool,
        api_key: str,
        verify_ssl: bool,
    ) -> None:
        self._session = async_get_clientsession(hass, verify_ssl)
        scheme = "https" if ssl else "http"
        self._base = f"{scheme}://{host}:{port}/api"
        self._api_key = api_key

    async def _call(self, mode: str) -> dict[str, Any]:
        params = {"mode": mode, "output": "json", "apikey": self._api_key}
        try:
            async with asyncio.timeout(10):
                resp = await self._session.get(self._base, params=params)
        except (TimeoutError, aiohttp.ClientError) as err:
            raise CannotConnect from err
        if resp.status in (401, 403):
            raise InvalidAuth
        if resp.status >= 400:
            raise CannotConnect
        return await resp.json(content_type=None)

    async def async_validate(self) -> None:
        """Validate connectivity + auth for the config flow."""
        await self._call("version")

    async def async_get_data(self) -> dict[str, Any]:
        """Fetch all monitored data."""
        queue = await self._call("queue")
        history = await self._call("history")
        version = await self._call("version")
        return {
            "queue": queue.get("queue", {}),
            "history": history.get("history", {}),
            "version": version.get("version"),
        }
