"""Sensor platform for NZBDav."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import EntityCategory, UnitOfDataRate, UnitOfInformation
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import NzbDavConfigEntry
from .coordinator import NzbDavCoordinator
from .entity import NzbDavEntity


def _failed_count(data: dict[str, Any]) -> int:
    slots = data.get("history", {}).get("slots", [])
    return sum(1 for s in slots if s.get("status") == "Failed")


def _status(data: dict[str, Any]) -> str:
    queue = data.get("queue", {})
    if queue.get("paused"):
        return "Paused"
    return queue.get("status", "Unknown")


@dataclass(frozen=True, kw_only=True)
class NzbDavSensorDescription(SensorEntityDescription):
    """Describes an NZBDav sensor."""

    value_fn: Callable[[dict[str, Any]], Any]


SENSORS: tuple[NzbDavSensorDescription, ...] = (
    NzbDavSensorDescription(
        key="status", translation_key="status", value_fn=_status,
    ),
    NzbDavSensorDescription(
        key="download_speed", translation_key="download_speed",
        native_unit_of_measurement=UnitOfDataRate.KILOBYTES_PER_SECOND,
        device_class=SensorDeviceClass.DATA_RATE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda d: float(d.get("queue", {}).get("kbpersec", 0.0)),
    ),
    NzbDavSensorDescription(
        key="queue_items", translation_key="queue_items",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda d: int(d.get("queue", {}).get("noofslots", 0)),
    ),
    NzbDavSensorDescription(
        key="remaining_size", translation_key="remaining_size",
        native_unit_of_measurement=UnitOfInformation.MEGABYTES,
        device_class=SensorDeviceClass.DATA_SIZE,
        value_fn=lambda d: float(d.get("queue", {}).get("mbleft", 0.0)),
    ),
    NzbDavSensorDescription(
        key="total_size", translation_key="total_size",
        native_unit_of_measurement=UnitOfInformation.MEGABYTES,
        device_class=SensorDeviceClass.DATA_SIZE,
        value_fn=lambda d: float(d.get("queue", {}).get("mb", 0.0)),
    ),
    NzbDavSensorDescription(
        key="time_left", translation_key="time_left",
        value_fn=lambda d: d.get("queue", {}).get("timeleft"),
    ),
    NzbDavSensorDescription(
        key="history_count", translation_key="history_count",
        state_class=SensorStateClass.TOTAL,
        value_fn=lambda d: int(d.get("history", {}).get("noofslots", 0)),
    ),
    NzbDavSensorDescription(
        key="failed_count", translation_key="failed_count",
        state_class=SensorStateClass.TOTAL,
        value_fn=_failed_count,
    ),
    NzbDavSensorDescription(
        key="version", translation_key="version",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda d: d.get("version"),
    ),
    NzbDavSensorDescription(
        key="disk_free", translation_key="disk_free",
        native_unit_of_measurement=UnitOfInformation.GIGABYTES,
        device_class=SensorDeviceClass.DATA_SIZE,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda d: float(d["queue"]["diskspace1"])
        if d.get("queue", {}).get("diskspace1") is not None else None,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: NzbDavConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator = entry.runtime_data
    async_add_entities(
        NzbDavSensor(coordinator, entry.entry_id, desc) for desc in SENSORS
    )


class NzbDavSensor(NzbDavEntity, SensorEntity):
    """A single NZBDav sensor."""

    entity_description: NzbDavSensorDescription

    def __init__(
        self,
        coordinator: NzbDavCoordinator,
        entry_id: str,
        description: NzbDavSensorDescription,
    ) -> None:
        super().__init__(coordinator, entry_id)
        self.entity_description = description
        self._attr_unique_id = f"{entry_id}_{description.key}"

    @property
    def native_value(self) -> Any:
        return self.entity_description.value_fn(self.coordinator.data)
