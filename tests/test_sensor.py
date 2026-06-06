"""Tests for NZBDav sensors via full entry setup."""
from __future__ import annotations

from unittest.mock import patch

from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.nzbdav.const import DOMAIN

ENTRY_DATA = {
    "host": "1.2.3.4", "port": 3000, "ssl": False,
    "api_key": "KEY", "verify_ssl": True,
}
FAKE = {
    "queue": {"status": "Downloading", "paused": False, "kbpersec": "1024.0",
              "mbleft": "100.0", "mb": "200.0", "timeleft": "0:01:00",
              "noofslots": 2, "slots": [{}, {}], "diskspace1": "50.0"},
    "history": {"noofslots": 5,
                "slots": [{"status": "Completed"}, {"status": "Failed"}]},
    "version": "0.6.4",
}


async def _setup(hass: HomeAssistant) -> MockConfigEntry:
    entry = MockConfigEntry(domain=DOMAIN, data=ENTRY_DATA)
    entry.add_to_hass(hass)
    with patch(
        "custom_components.nzbdav.NzbDavClient.async_get_data",
        return_value=FAKE,
    ):
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()
    return entry


async def test_status_sensor(hass: HomeAssistant):
    await _setup(hass)
    state = hass.states.get("sensor.nzbdav_status")
    assert state is not None
    assert state.state == "Downloading"


async def test_failed_count_sensor(hass: HomeAssistant):
    await _setup(hass)
    state = hass.states.get("sensor.nzbdav_failed_count")
    assert state.state == "1"


async def test_version_sensor(hass: HomeAssistant):
    await _setup(hass)
    state = hass.states.get("sensor.nzbdav_version")
    assert state.state == "0.6.4"


async def test_connectivity_binary_sensor(hass):
    await _setup(hass)
    state = hass.states.get("binary_sensor.nzbdav_connectivity")
    assert state is not None
    assert state.state == "on"
