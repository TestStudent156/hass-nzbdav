"""Tests for the NZBDav coordinator."""
from __future__ import annotations

from unittest.mock import AsyncMock

import pytest
from homeassistant.helpers.update_coordinator import UpdateFailed

from custom_components.nzbdav.api import CannotConnect
from custom_components.nzbdav.coordinator import NzbDavCoordinator


async def test_coordinator_returns_data(hass):
    client = AsyncMock()
    client.async_get_data.return_value = {"queue": {"status": "Idle"},
                                          "history": {}, "version": "1.0"}
    coord = NzbDavCoordinator(hass, client, scan_interval=30)
    data = await coord._async_update_data()
    assert data["queue"]["status"] == "Idle"


async def test_coordinator_wraps_errors(hass):
    client = AsyncMock()
    client.async_get_data.side_effect = CannotConnect
    coord = NzbDavCoordinator(hass, client, scan_interval=30)
    with pytest.raises(UpdateFailed):
        await coord._async_update_data()
