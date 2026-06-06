"""Tests for the NZBDav API client."""
from __future__ import annotations

import pytest
from aioresponses import aioresponses

from custom_components.nzbdav.api import (
    CannotConnect,
    InvalidAuth,
    NzbDavClient,
)


@pytest.fixture
def client(hass):
    return NzbDavClient(
        hass=hass, host="1.2.3.4", port=3000, ssl=False,
        api_key="KEY", verify_ssl=True,
    )


async def test_get_data_success(client):
    base = "http://1.2.3.4:3000/api"
    with aioresponses() as m:
        m.get(
            f"{base}?mode=queue&output=json&apikey=KEY",
            payload={"queue": {"status": "Downloading", "paused": False,
                                "kbpersec": "1024.0", "mbleft": "100.0",
                                "mb": "200.0", "timeleft": "0:01:00",
                                "noofslots": 2, "slots": [{}, {}],
                                "diskspace1": "50.0"}},
        )
        m.get(
            f"{base}?mode=history&output=json&apikey=KEY",
            payload={"history": {"noofslots": 5,
                                  "slots": [{"status": "Completed"},
                                            {"status": "Failed"}]}},
        )
        m.get(
            f"{base}?mode=version&output=json&apikey=KEY",
            payload={"version": "0.6.4"},
        )
        data = await client.async_get_data()

    assert data["queue"]["status"] == "Downloading"
    assert data["history"]["noofslots"] == 5
    assert data["version"] == "0.6.4"


async def test_invalid_auth_raises(client):
    with aioresponses() as m:
        m.get(
            "http://1.2.3.4:3000/api?mode=version&output=json&apikey=KEY",
            status=401,
        )
        with pytest.raises(InvalidAuth):
            await client.async_validate()


async def test_cannot_connect_raises(client):
    with aioresponses() as m:
        m.get(
            "http://1.2.3.4:3000/api?mode=version&output=json&apikey=KEY",
            exception=TimeoutError(),
        )
        with pytest.raises(CannotConnect):
            await client.async_validate()
