"""Binary sensor platform for NZBDav."""
from __future__ import annotations

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import NzbDavConfigEntry
from .entity import NzbDavEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: NzbDavConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    async_add_entities([NzbDavConnectivity(entry.runtime_data, entry.entry_id)])


class NzbDavConnectivity(NzbDavEntity, BinarySensorEntity):
    """Reports whether the last poll succeeded."""

    _attr_device_class = BinarySensorDeviceClass.CONNECTIVITY
    _attr_translation_key = "connectivity"

    def __init__(self, coordinator, entry_id: str) -> None:
        super().__init__(coordinator, entry_id)
        self._attr_unique_id = f"{entry_id}_connectivity"

    @property
    def is_on(self) -> bool:
        return self.coordinator.last_update_success
