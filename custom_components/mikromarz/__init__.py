"""Init"""
import asyncio
import json
import logging
from datetime import timedelta
from typing import Any, Dict, Optional, List
from async_timeout import timeout

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_HOST,
    CONF_PASSWORD,
    Platform,
)
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, DATA_COORDINATOR, SPLIT_CHAR, POS_DEVNAME, ValIndex
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .mikromarz_api import MikromarzApi
from .model import data_line_convert, get_meta, convert_units, get_device_attrs

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up rohlik integration from a config entry."""
    host = entry.data[CONF_HOST]
    """Set up platform from a ConfigEntry."""
    hass.data.setdefault(DOMAIN, {})

    api = MikromarzApi(host)
    coordinator = MikromarzDataUpdateCoordinator(hass, api)
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {DATA_COORDINATOR: coordinator}

    hass.config_entries.async_setup_platforms(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


class MikromarzDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Rohlik data."""
    api: MikromarzApi

    data = None
    converted = None
    device_name: str

    def __init__(
        self,
        hass,
        api: MikromarzApi,
    ):
        self.api = api
        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=timedelta(seconds=5))

    def _update_data(self) -> None:
        """Fetch data from Mikromarz via sync functions."""
        self.data = self.api.get_data()
        _LOGGER.debug("Mikromarz data: %s", self.data)

        data_arr = self.data.split(SPLIT_CHAR)
        self.device_name = data_arr[POS_DEVNAME]
        vals = []
        for x in range(len(data_arr)):
            vals.append(data_line_convert(data_arr, x))

        meta = get_meta(self.device_name)

        self.converted = [None for e in range(13)]

        for signal in get_device_attrs(self.device_name):
            index = signal.value
            self.converted[index] = convert_units(vals[index], meta[1][index])

    async def _async_update_data(self) -> None:
        """Fetch data from Mikromarz."""
        try:
            async with timeout(10):
                await self.hass.async_add_executor_job(self._update_data)
        except ConnectionError as error:
            self.data = None
            self.converted = None
            raise UpdateFailed(error) from error
