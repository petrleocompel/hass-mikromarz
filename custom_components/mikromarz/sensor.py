"""GitHub sensor platform."""
from datetime import timedelta, datetime
import logging

from homeassistant.core import callback
from homeassistant.helpers.entity import DeviceInfo

from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant import config_entries, core
from homeassistant.components.sensor import SensorEntity, SensorDeviceClass, SensorStateClass
import voluptuous as vol
from . import MikromarzDataUpdateCoordinator
from homeassistant.helpers import device_registry as dr


from .const import (
    DOMAIN, DATA_COORDINATOR, ValIndex, ValIndexPM2
)

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=10)


async def async_setup_entry(
    hass: core.HomeAssistant,
    entry: config_entries.ConfigEntry,
    async_add_entities,
):
    coordinator: MikromarzDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id][DATA_COORDINATOR]
    await coordinator.async_config_entry_first_refresh()

    sensors = []
    device_registry = dr.async_get(hass)
    device_registry.async_get_or_create(
        config_entry_id=entry.entry_id,
        identifiers={(DOMAIN, str(coordinator.api.ip))},
        manufacturer="Mikromarz",
        name="NT3-DN4",
    )
    if coordinator.device_name == "SE1-PM1":
        sensors.append(MikromarzEnergy(coordinator, ValIndex.ENERGY1, "Energy phase 1"))
        sensors.append(MikromarzEnergy(coordinator, ValIndex.ENERGY2, "Energy phase 2"))
        sensors.append(MikromarzEnergy(coordinator, ValIndex.ENERGY3, "Energy phase 3"))
        sensors.append(MikromarzEnergy(coordinator, ValIndex.TOTAL_ENERGY, "Total energy"))
        sensors.append(MikromarzPower(coordinator, ValIndex.POWER1, "Power phase 1"))
        sensors.append(MikromarzPower(coordinator, ValIndex.POWER2, "Power phase 2"))
        sensors.append(MikromarzPower(coordinator, ValIndex.POWER3, "Power phase 3"))
        sensors.append(MikromarzPower(coordinator, ValIndex.TOTAL_POWER, "Total power"))
    elif coordinator.device_name == "SE1-PM2":
        sensors.append(MikromarzEnergy(coordinator, ValIndexPM2.ENERGY1T1, "Energy phase 1"))
        sensors.append(MikromarzEnergy(coordinator, ValIndexPM2.ENERGY2T1, "Energy phase 2"))
        sensors.append(MikromarzEnergy(coordinator, ValIndexPM2.ENERGY3T1, "Energy phase 3"))
        sensors.append(MikromarzEnergy(coordinator, ValIndexPM2.TOTAL_ENERGYT1, "Total energy"))
        sensors.append(MikromarzPower(coordinator, ValIndexPM2.POWER1, "Power phase 1"))
        sensors.append(MikromarzPower(coordinator, ValIndexPM2.POWER2, "Power phase 2"))
        sensors.append(MikromarzPower(coordinator, ValIndexPM2.POWER3, "Power phase 3"))
        sensors.append(MikromarzPower(coordinator, ValIndexPM2.TOTAL_POWER, "Total power"))

    async_add_entities(sensors, update_before_add=True)




class MikromarzPower(CoordinatorEntity, SensorEntity):
    _attr_device_class = SensorDeviceClass.POWER
    _attr_has_entity_name = True
    _val_index: ValIndex
    _name: str

    """Representation of Hikvision external magnet detector."""
    coordinator: MikromarzDataUpdateCoordinator

    _ref_id: str

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        return DeviceInfo(
            identifiers={(DOMAIN, str(self._ref_id))},
            manufacturer="Mikromarz",
            name="NT3-DN4",
        )

    def __init__(self, coordinator: MikromarzDataUpdateCoordinator, value_index: ValIndex, name: str, is_total: bool = False) -> None:
        """Create the entity with a DataUpdateCoordinator."""
        super().__init__(coordinator)
        self._ref_id = coordinator.api.ip
        self._attr_unique_id = "mikromarz_power_" + str(value_index.value)
        self._attr_icon = "mdi:flash"
        self._attr_native_unit_of_measurement = "W"
        self._val_index = value_index
        self._name = name
        self._attr_has_entity_name = True
        if is_total:
            self._attr_state_class = SensorStateClass.TOTAL_INCREASING
        else:
            self._attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def name(self) -> str:
        return self._name


    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()
        if self.coordinator.converted is not None:
            self._attr_native_value = self.coordinator.converted[self._val_index.value]


class MikromarzEnergy(CoordinatorEntity, SensorEntity):
    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_has_entity_name = True
    _val_index: ValIndex
    _name: str

    """Representation of Hikvision external magnet detector."""
    coordinator: MikromarzDataUpdateCoordinator

    _ref_id: str

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        return DeviceInfo(
            identifiers={(DOMAIN, str(self._ref_id))},
            manufacturer="Mikromarz",
            name="NT3-DN4",
        )

    def __init__(self, coordinator: MikromarzDataUpdateCoordinator, value_index: ValIndex, name: str, is_total: bool = False) -> None:
        """Create the entity with a DataUpdateCoordinator."""
        super().__init__(coordinator)
        self._ref_id = coordinator.api.ip
        self._attr_unique_id = "mikromarz_energy_" + str(value_index.value)
        self._attr_icon = "mdi:flash"
        self._attr_native_unit_of_measurement = "kWh"
        self._val_index = value_index
        self._name = name
        self._attr_has_entity_name = True
        if is_total:
            self._attr_state_class = SensorStateClass.TOTAL_INCREASING
        else:
            self._attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def name(self) -> str:
        return self._name

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()
        if self.coordinator.converted is not None:
            self._attr_native_value = self.coordinator.converted[self._val_index.value] / 1000

